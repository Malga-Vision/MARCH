import re
from pathlib import Path

import pandas as pd


class User_Case_Dataset_NumPy:
    """
    legend:
        user_labels = [0, ..., 49] participant ID
        case_labels = [1, ..., 7] case type
        tool_labels = [0, 1]
            tool_labels == 0 -> IMUs
            tool_labels == 1 -> Samsung smartphone
        
        for tool_labels == 0:
            data_id = [0, 1, 2, 3]
            data_id[0] == imu_0
            data_id[1] == imu_1
            data_id[2] == imu_2
            data_id[3] == imu_3
        
        for tool_labels == 1: data_id = [0]

    data legend:
        data:
            data[:, 0] -> timestamp_ns (ns=nano seconds)
            data[:, 1] -> angular velocity x (wx)
            data[:, 2] -> angular velocity y (wy)
            data[:, 3] -> angular velocity z (wz)
            data[:, 4] -> acceleration x (ax)
            data[:, 5] -> acceleration y (ay)
            data[:, 6] -> acceleration z (az)
            data[:, 7] -> gravity x (gx)
            data[:, 8] -> gravity y (gy)
            data[:, 9] -> gravity z (gz)
            data[:, 10] -> time_ms_loc (local time in milliseconds)
        
    input:
        root_dir = folder with all segments 

    return:
            data: numpy.array
            label user
            label case
            label tool
            label data_id
    """

    TOOL_LABELS = {
        "IMUs": 0,
        "Samsung": 1,
    }

    SENSOR_IDS = {
        "IMUs": {
            "imu_0_data_sync.csv": 0,
            "imu_1_data_sync.csv": 1,
            "imu_2_data_sync.csv": 2,
            "imu_3_data_sync.csv": 3,
        },
        "Samsung": {
            "Samsung_sync.csv": 0,
        },
    }

    USER_PATTERN = re.compile(r"^user_(\d+)_sync$")
    CASE_PATTERN = re.compile(r"^case_(\d+)$")

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir).expanduser().resolve()
        if not self.root_dir.is_dir():
            raise FileNotFoundError(f"Dataset root directory not found: {self.root_dir}")

        self.users = []
        self.users_to_idx = {}
        self.cases = {}
        self.case_to_idx = {}
        self.instrument = {}
        self.instrument_to_idx = {}
        self.data_type = {}
        self.data_type_to_idx = {}

        self.data_paths = []
        self.user_labels = []
        self.case_labels = []
        self.tool_labels = []
        self.data_ids = []

        for user_path in sorted(path for path in self.root_dir.iterdir() if path.is_dir()):
            user_label = self._label_from_pattern(self.USER_PATTERN, user_path.name)
            if user_label is None:
                continue

            user = user_path.name
            self.users.append(user)
            self.users_to_idx[user] = user_label
            self.cases[user] = []
            self.case_to_idx[user] = {}
            self.instrument[user] = {}
            self.instrument_to_idx[user] = {}
            self.data_type[user] = {}
            self.data_type_to_idx[user] = {}

            for case_path in sorted(path for path in user_path.iterdir() if path.is_dir()):
                case_label = self._label_from_pattern(self.CASE_PATTERN, case_path.name)
                if case_label is None:
                    continue

                case = case_path.name
                self.cases[user].append(case)
                self.case_to_idx[user][case] = case_label
                self.instrument[user][case] = []
                self.instrument_to_idx[user][case] = {}
                self.data_type[user][case] = {}
                self.data_type_to_idx[user][case] = {}

                for tool_name, tool_label in self.TOOL_LABELS.items():
                    instrument_path = case_path / tool_name
                    if not instrument_path.is_dir():
                        continue

                    sensor_ids = self.SENSOR_IDS[tool_name]
                    data_files = sorted(
                        path.name
                        for path in instrument_path.iterdir()
                        if path.is_file() and path.name in sensor_ids
                    )

                    self.instrument[user][case].append(tool_name)
                    self.instrument_to_idx[user][case][tool_name] = tool_label
                    self.data_type[user][case][tool_name] = data_files
                    self.data_type_to_idx[user][case][tool_name] = {
                        data_file: sensor_ids[data_file] for data_file in data_files
                    }

                    for data_file in data_files:
                        self.data_paths.append(instrument_path / data_file)
                        self.user_labels.append(user_label)
                        self.case_labels.append(case_label)
                        self.tool_labels.append(tool_label)
                        self.data_ids.append(sensor_ids[data_file])

    def __len__(self):
        return len(self.data_paths)

    def __getitem__(self, idx):
        data_path = self.data_paths[idx]
        data_df = pd.read_csv(data_path)

        return (
            data_df.to_numpy(copy=False),
            self.user_labels[idx],
            self.case_labels[idx],
            self.tool_labels[idx],
            self.data_ids[idx]
        )

    @staticmethod
    def _label_from_pattern(pattern, name):
        match = pattern.match(name)
        if match is None:
            return None
        return int(match.group(1))
