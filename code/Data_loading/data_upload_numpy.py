from pathlib import Path

import numpy as np

from dataset_numpy import User_Case_Dataset_NumPy
from utility import get_selection_config, variable_selection_numpy


def main():
    repo_root = Path(__file__).resolve().parents[2]
    data_path = repo_root / "data"

    dataset = User_Case_Dataset_NumPy(data_path)

    users, cases, tools, ids = get_selection_config()
    all_data, all_user, all_cases, all_tool, all_ids = variable_selection_numpy(dataset, users, cases, tools, ids)
    if all_data is None:
        return

    print(f"Loaded data shape: {all_data.shape}")
    print(f"Users: {np.unique(all_user).tolist()}")
    print(f"Cases: {np.unique(all_cases).tolist()}")
    print(f"Tools: {np.unique(all_tool).tolist()}")
    print(f"Sensor IDs: {np.unique(all_ids).tolist()}")


if __name__ == "__main__":
    main()
