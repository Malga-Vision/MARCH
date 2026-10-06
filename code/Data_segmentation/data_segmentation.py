"""Segment and compare inertial signals for one user and walking case."""

import argparse
import io
import pickle
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


FUNCTIONS_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = FUNCTIONS_ROOT.parent
DATA_ROOT = REPO_ROOT / "Data"
INDICES_ROOT = Path(__file__).resolve().with_name("Indices")
OUTPUT_PATH = Path(__file__).resolve().with_name("segments_plot.png")

# Make direct execution work from any current working directory.
if str(FUNCTIONS_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTIONS_ROOT))

from Data_loading.dataset_numpy import User_Case_Dataset_NumPy


@dataclass(frozen=True)
class SensorConfig:
    title: str
    tool: int
    sensor_id: int
    boundary_file: str


# The numeric IDs preserve the ordering used by the old imu_0 ... imu_3 files.
SENSORS = (
    SensorConfig("IMU RL", 0, 0, "indices_dictionary_segments_imu_1.pkl"),
    SensorConfig("IMU RA", 0, 1, "indices_dictionary_segments_imu_1.pkl"),
    SensorConfig("IMU LL", 0, 2, "indices_dictionary_segments_imu_3.pkl"),
    SensorConfig("IMU LA", 0, 3, "indices_dictionary_segments_imu_3.pkl"),
    SensorConfig("Smartphone", 1, 0, "indices_dictionary_segments_imu_3.pkl"),
)

SIGNALS = (
    ("acceleration", slice(4, 7), r"$|a|$"),
    ("angular_velocity", slice(1, 4), r"$|\omega|$"),
)


class _StorageUnpickler(pickle.Unpickler):
    """Read storage metadata embedded by legacy Torch pickles."""

    def find_class(self, module, name):
        if module == "torch" and name.endswith("Storage"):
            return type(name, (), {})
        return super().find_class(module, name)

    def persistent_load(self, persistent_id):
        storage_kind, storage_type, _, _, count, _ = persistent_id
        if storage_kind != "storage":
            raise pickle.UnpicklingError(
                f"Unsupported Torch persistent object: {storage_kind!r}"
            )
        return storage_type.__name__, count


def _load_torch_storage(payload):
    """Convert one legacy Torch storage payload to a NumPy array."""

    stream = io.BytesIO(payload)
    unpickler = _StorageUnpickler(stream)
    unpickler.load()  # serialization magic number
    unpickler.load()  # protocol version
    system_info = unpickler.load()
    storage_type, expected_count = unpickler.load()
    unpickler.load()  # storage keys

    byte_order = "<" if system_info.get("little_endian", True) else ">"
    count_bytes = stream.read(8)
    if len(count_bytes) != 8:
        raise pickle.UnpicklingError("Truncated Torch storage header")
    stored_count = struct.unpack(f"{byte_order}q", count_bytes)[0]
    if stored_count != expected_count:
        raise pickle.UnpicklingError(
            f"Torch storage size mismatch: {stored_count} != {expected_count}"
        )

    dtypes = {
        "DoubleStorage": "f8",
        "FloatStorage": "f4",
        "LongStorage": "i8",
        "IntStorage": "i4",
    }
    try:
        dtype = np.dtype(f"{byte_order}{dtypes[storage_type]}")
    except KeyError as exc:
        raise pickle.UnpicklingError(
            f"Unsupported Torch storage type: {storage_type}"
        ) from exc

    raw_values = stream.read(stored_count * dtype.itemsize)
    if len(raw_values) != stored_count * dtype.itemsize:
        raise pickle.UnpicklingError("Truncated Torch storage payload")
    return np.frombuffer(raw_values, dtype=dtype, count=stored_count).copy()


def _rebuild_torch_tensor(storage, offset, size, stride, *_):
    """Rebuild the dense tensors used by the boundary dictionaries."""

    shape = tuple(size)
    element_strides = tuple(stride)
    if len(shape) != len(element_strides):
        raise pickle.UnpicklingError("Invalid Torch tensor shape/stride metadata")

    required_values = offset + max(
        sum((length - 1) * step for length, step in zip(shape, element_strides))
        + 1,
        0,
    )
    if required_values > storage.size:
        raise pickle.UnpicklingError("Torch tensor exceeds its backing storage")

    byte_strides = tuple(step * storage.dtype.itemsize for step in element_strides)
    return np.lib.stride_tricks.as_strided(
        storage[offset:], shape=shape, strides=byte_strides
    ).copy()


class _TorchCompatibleUnpickler(pickle.Unpickler):
    """Unpickle the supplied legacy Torch tensors without importing Torch."""

    def find_class(self, module, name):
        if (module, name) == ("torch.storage", "_load_from_bytes"):
            return _load_torch_storage
        if (module, name) == ("torch._utils", "_rebuild_tensor_v2"):
            return _rebuild_torch_tensor
        return super().find_class(module, name)


def load_boundaries(path, user, case):
    """Load and validate cycle-boundary timestamps for a user and case."""

    path = Path(path)
    with path.open("rb") as file:
        boundary_dictionary = _TorchCompatibleUnpickler(file).load()

    try:
        boundaries = np.asarray(boundary_dictionary[user][case], dtype=np.float64)
    except KeyError as exc:
        raise KeyError(
            f"No segmentation boundaries for user {user}, case {case} in {path}"
        ) from exc

    if boundaries.ndim != 1 or boundaries.size < 2:
        raise ValueError(f"Expected at least two boundary timestamps in {path}")
    if np.any(np.diff(boundaries) <= 0):
        raise ValueError(f"Boundary timestamps are not strictly increasing in {path}")
    return boundaries


def find_recording(dataset, user, case, tool, sensor_id):
    """Return a recording by labels, independently of directory ordering."""

    matches = [
        index
        for index in range(len(dataset))
        if dataset.user_labels[index] == user
        and dataset.case_labels[index] == case
        and dataset.tool_labels[index] == tool
        and dataset.data_ids[index] == sensor_id
    ]
    if not matches:
        raise LookupError(
            "Recording not found for "
            f"user={user}, case={case}, tool={tool}, sensor_id={sensor_id}"
        )
    if len(matches) > 1:
        paths = ", ".join(str(dataset.data_paths[index]) for index in matches)
        raise LookupError(f"Multiple recordings match the requested labels: {paths}")
    return dataset[matches[0]][0]


def resample_segment(segment, sample_count):
    """Linearly resample a one-dimensional segment to a fixed length."""

    segment = np.asarray(segment, dtype=np.float64)
    if segment.size < 2:
        raise ValueError("Cannot resample a segment containing fewer than two samples")
    source = np.linspace(0.0, 1.0, num=segment.size)
    target = np.linspace(0.0, 1.0, num=sample_count)
    return np.interp(target, source, segment)


def segment_signal(
    data, boundaries, columns, sample_count=100, edge_cycles=1, resample=True
):
    """Split a vector magnitude at timestamps, optionally resampling each cycle."""

    data = np.asarray(data)
    if data.ndim != 2 or data.shape[1] < 7:
        raise ValueError(f"Expected an N x 7 sensor array, received {data.shape}")
    if resample and sample_count < 2:
        raise ValueError("sample_count must be at least 2")
    if edge_cycles < 0:
        raise ValueError("edge_cycles cannot be negative")

    timestamps = np.asarray(data[:, 0], dtype=np.float64)
    if timestamps.size < 2:
        raise ValueError("Recording contains fewer than two samples")
    if np.any(np.diff(timestamps) < 0):
        raise ValueError("Recording timestamps are not sorted")

    # Keep only boundaries inside this sensor's interval. np.split then creates
    # leading/trailing partial segments; those are excluded with [1:-1].
    boundaries = np.asarray(boundaries, dtype=np.float64)
    boundaries = boundaries[
        (boundaries > timestamps[0]) & (boundaries < timestamps[-1])
    ]
    if boundaries.size < 2:
        raise ValueError("Fewer than two segmentation boundaries overlap the recording")

    split_indices = np.unique(np.searchsorted(timestamps, boundaries))
    magnitude = np.linalg.norm(
        np.asarray(data[:, columns], dtype=np.float64), axis=1
    )
    complete_cycles = [
        segment
        for segment in np.split(magnitude, split_indices)[1:-1]
        if segment.size >= 2
    ]
    if edge_cycles:
        if len(complete_cycles) <= 2 * edge_cycles:
            raise ValueError("Too few complete cycles after dropping edge cycles")
        complete_cycles = complete_cycles[edge_cycles:-edge_cycles]
    if not complete_cycles:
        raise ValueError("No complete cycles could be segmented")

    if not resample:
        return complete_cycles

    return np.vstack(
        [resample_segment(segment, sample_count) for segment in complete_cycles]
    )


def collect_segments(
    dataset,
    user=7,
    case=4,
    sample_count=100,
    edge_cycles=1,
    indices_root=INDICES_ROOT,
    resample=True,
):
    """Build acceleration and angular-velocity segments for every sensor."""

    boundary_cache = {}
    samples = {signal_name: {} for signal_name, _, _ in SIGNALS}

    for sensor in SENSORS:
        boundary_path = Path(indices_root) / sensor.boundary_file
        if boundary_path not in boundary_cache:
            boundary_cache[boundary_path] = load_boundaries(
                boundary_path, user=user, case=case
            )

        data = find_recording(
            dataset,
            user=user,
            case=case,
            tool=sensor.tool,
            sensor_id=sensor.sensor_id,
        )
        for signal_name, columns, _ in SIGNALS:
            samples[signal_name][sensor.title] = segment_signal(
                data,
                boundary_cache[boundary_path],
                columns,
                sample_count=sample_count,
                edge_cycles=edge_cycles,
                resample=resample,
            )

    return samples


def average_segments(segments):
    """Average variable-length cycles without changing their sample spacing."""

    segment_arrays = [np.asarray(segment, dtype=np.float64) for segment in segments]
    if not segment_arrays:
        raise ValueError("Cannot average an empty collection of segments")

    maximum_length = max(segment.size for segment in segment_arrays)
    padded_segments = np.full(
        (len(segment_arrays), maximum_length), np.nan, dtype=np.float64
    )
    for index, segment in enumerate(segment_arrays):
        padded_segments[index, : segment.size] = segment

    return np.nanmean(padded_segments, axis=0)


def plot_segments(samples, user, case, resample=True):
    """Plot segmented cycles and their average for each sensor."""

    figure, axes = plt.subplots(
        len(SENSORS), len(SIGNALS), figsize=(20, 15), sharex=True, squeeze=False
    )

    for column, (signal_name, _, y_label) in enumerate(SIGNALS):
        for row, sensor in enumerate(SENSORS):
            axis = axes[row, column]
            segments = samples[signal_name][sensor.title]

            for index, segment in enumerate(segments):
                label = (
                    f"{len(segments)} raw cycles"
                    if not resample and index == 0
                    else None
                )
                axis.plot(segment, alpha=0.35, linewidth=0.8, label=label)

            average_segment = average_segments(segments)
            axis.plot(
                average_segment,
                "--",
                linewidth=2,
                color="black",
                label=f"average ({len(segments)} cycles)",
            )

            axis.set_title(sensor.title, size=16)
            x_label = "Normalized time index" if resample else "Sample index"
            axis.set_xlabel(x_label, size=12)
            axis.set_ylabel(y_label, size=12)
            axis.grid(True, alpha=0.3)
            axis.legend()

    mode = "Resampled" if resample else "Raw"
    figure.suptitle(f"{mode} segments by sensor - user {user}, case {case}", size=20)
    figure.tight_layout(rect=[0, 0, 1, 0.96])
    return figure


def main(
    user=7,
    case=4,
    sample_count=100,
    edge_cycles=1,
    data_root=DATA_ROOT,
    indices_root=INDICES_ROOT,
    output_path=OUTPUT_PATH,
    show=True,
    resample=True,
):
    dataset = User_Case_Dataset_NumPy(data_root)
    samples = collect_segments(
        dataset,
        user=user,
        case=case,
        sample_count=sample_count,
        edge_cycles=edge_cycles,
        indices_root=indices_root,
        resample=resample,
    )
    figure = plot_segments(
        samples, user=user, case=case, resample=resample
    )

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150)
        print(f"Saved segmentation plot to {output_path}")
    if show:
        plt.show()
    else:
        plt.close(figure)
    return samples


def _parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", type=int, default=7)
    parser.add_argument("--case", type=int, default=4, choices=range(1, 8))
    parser.add_argument(
        "--samples",
        type=int,
        default=100,
        help="samples per cycle when resampling (default: 100)",
    )
    parser.add_argument(
        "--no-resample",
        dest="resample",
        action="store_false",
        help="keep cycles at their original lengths",
    )
    parser.add_argument(
        "--edge-cycles",
        type=int,
        default=1,
        help="complete cycles to discard at each edge (default: 1)",
    )
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--indices-root", type=Path, default=INDICES_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--no-show", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_arguments()
    main(
        user=arguments.user,
        case=arguments.case,
        sample_count=arguments.samples,
        edge_cycles=arguments.edge_cycles,
        resample=arguments.resample,
        data_root=arguments.data_root,
        indices_root=arguments.indices_root,
        output_path=arguments.output,
        show=not arguments.no_show,
    )
