import os
import numpy as np
import pandas as pd
from pathlib import Path

class User_Case_Dataset_NumPy:
    '''
    legend:
        user_labels = [0, ..., n] with n number of users
        case_labels = [1, ..., 7] case type
        tool_labels = [0, 1, 2]
            tool_labels[0] = IMUs
            tool_labels[1] = Sensor_logger
            tool_labels[2] = User_phone
        
        for tool_labels == 0:
            data_id = [0, 1, 2, 3]
            data_id[0] == imu_0
            data_id[1] == imu_1
            data_id[2] == imu_2
            data_id[3] == imu_3
        
        for tool_labes == 1: data_id=[0]

    data legend:
        data:
            seg[:, :, 0] -> timestamp_ns (ns=nano seconds)
            seg[:, :, 1] -> angular velocity x(wx)
            seg[:, :, 2] -> angular velocity y (wy)
            seg[:, :, 3] -> angular velocity z (wx)
            seg[:, :, 4] -> acceleration x (ax)
            seg[:, :, 5] -> acceleration y (ay)
            seg[:, :, 6] -> acceleration z (az)
            seg[:, :, 7] -> gravity x (gx)
            seg[:, :, 8] -> gravity y (gy)
            seg[:, :, 9] -> gravity z (gz)
            seg[:, :, 10] -> time_ms_loc (local time in milliseconds)
        
    input:
        root_dir = folder with all segments 

    return:
            data: numpy.array
            label user
            label case
            label tool
            label data_id
    '''
    def __init__(self, root_dir):
        # Ensure root_dir is a Path object so the '/' operator works
        self.root_dir = Path(root_dir)

        self.users = sorted(os.listdir(self.root_dir))
        self.users_to_idx = {user: idx for idx, user in enumerate(self.users)}

        self.cases = {}
        self.case_to_idx = {}

        self.instrument = {}
        self.instrument_to_idx = {}

        self.data_type = {}
        self.data_type_to_idx = {}

        # --- Directory Traversal (Same logic as before) ---
        for user in self.users:
            user_path = self.root_dir / user
            # Skip if it's not a directory
            if not os.path.isdir(user_path): continue
            
            cases_folder = sorted(os.listdir(user_path))
            self.cases[user] = cases_folder
            self.case_to_idx[user] = {case: idx for idx, case in enumerate(cases_folder)}

            self.instrument[user] = {}
            self.instrument_to_idx[user] = {}
            self.data_type[user] = {}
            self.data_type_to_idx[user] = {}

            for case in cases_folder:
                case_path = self.root_dir / user / case
                if not os.path.isdir(case_path): continue

                # Filter logic
                instrument_folder = [
                    tool for tool in filter(
                        lambda x: not x.startswith("App_Pro") and not x.startswith("ZED") and not x.endswith(".csv"), 
                        sorted(os.listdir(case_path))
                    )
                ]
                
                self.instrument[user][case] = instrument_folder
                self.instrument_to_idx[user][case] = {tool: idx for idx, tool in enumerate(instrument_folder)}

                self.data_type[user][case] = {}
                self.data_type_to_idx[user][case] = {}

                for instrument in instrument_folder:
                    inst_path = self.root_dir / user / case / instrument
                    if not os.path.isdir(inst_path): continue
                    
                    data_folder = sorted(os.listdir(inst_path))
                    self.data_type[user][case][instrument] = data_folder
                    self.data_type_to_idx[user][case][instrument] = {tool: idx for idx, tool in enumerate(data_folder)}

        # --- Flattening Paths ---
        self.data_paths = []
        self.user_labels = []
        self.case_labels = []
        self.tool_labels = []
        self.data_ids = []

        for user in self.users:
            if user not in self.cases: continue
            for case in self.cases[user]:
                for sensor in self.instrument[user][case]:
                    for data in self.data_type[user][case][sensor]:
                        data_path = self.root_dir / user / case / sensor / data
                        
                        self.data_paths.append(data_path)
                        self.user_labels.append(self.users_to_idx[user])
                        self.case_labels.append(self.case_to_idx[user][case])
                        self.tool_labels.append(self.instrument_to_idx[user][case][sensor])
                        self.data_ids.append(self.data_type_to_idx[user][case][sensor][data])

    def __len__(self):
        return len(self.data_paths)

    
    def __getitem__(self, idx):
        
        data_path = self.data_paths[idx]
        data_df = pd.read_csv(data_path)
        
        
        if isinstance(data_df, pd.DataFrame):
            data_array = data_df.values
        else:
            data_array = data_df

        
        return (
            data_array, 
            self.user_labels[idx], 
            self.case_labels[idx] + 1, 
            self.tool_labels[idx], 
            self.data_ids[idx]
        )