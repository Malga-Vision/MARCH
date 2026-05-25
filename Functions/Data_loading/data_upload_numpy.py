from pathlib import Path

from dataset_numpy import User_Case_Dataset_NumPy
import numpy as np
from utility import get_selection_config, variable_selection_numpy

def main():
    global_path = Path('../../Data/')

    dataset  = User_Case_Dataset_NumPy(global_path)

    users, cases, tools, ids = get_selection_config()
    all_data, all_user, all_cases, all_tool, all_ids = variable_selection_numpy(dataset, users, cases, tools, ids)
    print(all_data)
    
if __name__ == "__main__":
    main()