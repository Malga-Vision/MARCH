import pandas as pd 
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_prominences
import matplotlib.gridspec as gridspec
from scipy.constants import g

import os
import pickle


def load_imu(global_path, user, case, index):

    """ funzione upload imu"""

    folder = Path(global_path / user / f"{case}/IMUs")
    filename = next(filter(lambda x: x.endswith(f"{index}_data_sync.csv"), os.listdir(folder)))
    return pd.read_csv(folder / filename)

def parallel_load_imu(args):
    with ThreadPoolExecutor() as executor:
        imu_data = list(executor.map(lambda arg: load_imu(*arg), args))
    return imu_data


def g_segmenting(imu, user, case, distance):

    start = 0
    end = -1

    if np.abs(8.5 - np.mean(imu)) > 0.5:
        th_low = - np.mean(imu)
    
    else: th_low = -8.5

    th_up = 10
    # print(imu_1)
    ind, _ = find_peaks(- imu, threshold = 0, distance = distance, height = (th_low , th_up))#, height = (th_low , th_up)

    # t_seg, g_seg = np.split(imu_1['time_ms_loc'], ind), np.split(imu_1['gx'], ind)

    return imu.index[ind]


def main():
    dir_path = Path("../../data/")

    indices_dictionary = {}

    for user in sorted(os.listdir(dir_path)):
        
        cases_path = dir_path / user
        indices_dictionary[user] = {}
        
        for case in sorted(os.listdir(cases_path)):

            _, imu_1, _, imu_3 = parallel_load_imu([(dir_path, user, case, i) for i in range(4)])
            # if user == "user_19_sync": print(imu_1)
            # imu_1['ay'] = - imu_1['ay']
            
            ind = []
            # print(imu_1)
            for imu in np.array_split(imu_1["gx"], 10):
                # print(imu)
                # break
                ind.append(g_segmenting(imu, user, case, distance = 50))

            # salvo ind 
            ind = np.concatenate(ind)
            # print(user)
            # if user == "user_19_sync": print(imu_1)
            indices_dictionary[user][case] = ind

            ind = []
    # print(indices_dictionary)
    with open("/Indicies/indices_dictionary_sync_data_segments_imu_1_all.pkl", "wb") as f:
        pickle.dump(indices_dictionary, f)

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")