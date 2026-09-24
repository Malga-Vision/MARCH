from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "Data"
OUTPUT_PATH = Path(__file__).resolve().with_name("plot.png")


def main(user="user_00_sync", case="case_1", start=1000, end=1200):
    data_path = DATA_ROOT / user / case

    imu_right = pd.read_csv(data_path / "IMUs" / "IMU_RA_data_sync.csv")
    imu_left = pd.read_csv(data_path / "IMUs" / "IMU_LA_data_sync.csv")

    t_left = imu_left["time_ms_loc"].iloc[start:end]
    t_right = imu_right["time_ms_loc"].iloc[start:end]
    markersize = 2
    linewidth = 0.5

    groups = [
        (
            "Gravity",
            [("gx", "$g_x$"), ("gy", "$g_y$"), ("gz", "$g_z$")],
            r"$[\frac{m}{s^2}]$",
        ),
        (
            "Acceleration",
            [("ax", "$a_x$"), ("ay", "$a_y$"), ("az", "$a_z$")],
            r"$[\frac{m}{s^2}]$",
        ),
        (
            "Angular Velocity",
            [("wx", r"$\omega_x$"), ("wy", r"$\omega_y$"), ("wz", r"$\omega_z$")],
            r"$[\frac{rad}{s}]$",
        ),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle("Ankles IMU", fontsize=30, y=0.99)

    for row_idx, (title, signals, unit) in enumerate(groups):
        axes[row_idx, 1].set_title(title, fontsize=20, pad=20)

        for col_idx, (column, ylabel) in enumerate(signals):
            ax = axes[row_idx, col_idx]
            _configure_axis(ax, ylabel, unit)
            ax.plot(
                t_rigth,
                imu_right[column].iloc[start:end],
                "-o",
                markersize=markersize,
                linewidth=linewidth,
                label="right",
            )
            ax.plot(
                t_left,
                imu_left[column].iloc[start:end],
                "-o",
                markersize=markersize,
                linewidth=linewidth,
                label="left",
            )
            ax.legend()

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUTPUT_PATH)
    plt.show()


def _configure_axis(ax, ylabel, unit):
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_xlabel("$t$", fontsize=15)
    ax.tick_params(axis="both", labelsize=8)
    ax.text(
        1,
        0,
        "$[ms]$",
        horizontalalignment="left",
        verticalalignment="top",
        transform=ax.transAxes,
        fontsize=10,
    )
    ax.text(
        0,
        1,
        unit,
        horizontalalignment="right",
        verticalalignment="bottom",
        transform=ax.transAxes,
        fontsize=10,
    )


if __name__ == "__main__":
    main()
