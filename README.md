<!-- <p align="center">
  <img src="Figures/logo.png" width="550" title="hover text">
</p>

## The MARCH dataset: Multi-modal learning for gait-based human analysis and authentication


### Description and motivations

The MARCH dataset is a comprehensive and rich multimodal dataset composed of inertial and video data. This dataset aims to provide a rich and diverse description of different walking patterns. It will be rich because it includes a large number of individuals of various ages and genders. It will be diverse as it incorporates data from multiple devices, and various clothing styles, ensuring an appropriate level of variability. 

The dataset consists in 50 gender-balanced participants (26 males and 24 females), of age 26.8± 2.9 performing 7 different walks on a treadmill of 5 minutes each in indoor environment. During the first two trials, the treadmill velocity was fixed at 2 km/h. In the third and fourth trials, participants chose a comfortable walking speed. For the fifth and sixth trials, the speed remained user-selected; however, a one-kilogram weight was fastened to the participant's left ankle to simulate an injury. The seventh and final trial followed a pre-programmed speed profile. Every 30 seconds, the velocity shifted between a minimum of 2 km/h and a maximum of 5 km/h according to the following sequence (in km/h): (2,4,3,4,3,5,4,2,5,3).

Additionally, all even-numbered trials were conducted barefoot, while odd-numbered trials were performed with shoes. These conditions are summarised in the following Table.

<p align="center">
  <img src="Figures/data.png" width="550" title="hover text">
</p>

Each user worn five sensors, four IMUs and one smartphone.  Two IMUs were secured to the exterior of both ankles, while the remaining two were fastened to the exterior middle section of both thighs; all were held in place using Velcro straps. When the participant stood in a stationary position, the IMUs were oriented such that the x-axis was parallel to the leg (pointing downward), and the z-axis was parallel to the ground, pointing toward the inner part of the body. The y-axis was oriented according to the left-hand rule.

The Samsung smartphone was placed in the back-left pocket of the trousers with the y-axis oriented perpendicularly to the ground, the z-axis pointing toward the body, and the x-axis oriented according to the right-hand rule. 

The figure illustrates the IMU positions (red circles) and the Samsung smartphone placement (yellow circle)

<p align="center">
  <img src="Figures/position_cropped.png" width="550" title="hover text">
</p>

Additionally, we collected timestamps of all sensors simplifying the synchronisation across all devises. In total we collected 29.16 hours of data per sensor.

### Technical information: NumPy Data Structure

The User_Case_Dataset_NumPy class parses the dataset's directory tree (root_dir / user / case / instrument / data_file) and converts the raw CSV files into structured NumPy arrays.

Calling the dataset via its index (dataset[idx]) returns a tuple containing the sensor data matrix alongside its four corresponding identifying labels: (data_array, user_label, case_label, tool_label, data_id).

1. The Data Matrix (data_array)
Each returned data_array is a 2D NumPy array where rows represent continuous time samples and the 11 columns contain the specific kinematic values. The columns are structured exactly as follows:

    Col 0: timestamp_ns (System timestamp in nanoseconds)

    Col 1: wx (Angular velocity X)

    Col 2: wy (Angular velocity Y)

    Col 3: wz (Angular velocity Z)

    Col 4: ax (Linear acceleration X)

    Col 5: ay (Linear acceleration Y)

    Col 6: az (Linear acceleration Z)

    Col 7: gx (Gravity X)

    Col 8: gy (Gravity Y)

    Col 9: gz (Gravity Z)

    Col 10: time_ms_loc (Local time in milliseconds, used for synchronized plotting)

2. Label Encodings
To facilitate segmentation and machine learning training, the data is paired with integer-encoded labels. These guarantee you always know the exact context of the data_array:

    user_label [0 to n]: Identifies the specific subject performing the trial.

    case_label [1 to 7]: Identifies the specific gait scenario or testing condition being executed.

    tool_label [0 or 1]: Identifies the hardware system used for the capture:

      0 = Wearable IMUs

      1 = Smartphone (Sensor Logger App)

    data_id: Specifies the exact spatial location or identifier of the sensor:

      If tool_label == 0 (IMUs): Evaluates to 0, 1, 2, or 3 (imu_0 through imu_3).

      If tool_label == 1 (Smartphone): Evaluates to 0.

### Available functions
Loading and visualisation scripts allow users to access, filter, and plot the MARCH inertial data.

The data loading functions (get_selection_config and variable_selection_numpy) allow the user to load specific subsets of the MARCH dataset into easy-to-use NumPy arrays. You can filter the data by users, cases, tools (IMU vs. Smartphone), and specific sensor IDs.

Syntax & Data Loading:

get_selection_config(user_input, case_input, tool_input, id_input) parses your selection criteria. If arguments are omitted, it prompts the user for inputs interactively via the console.

  Users: Accepts 'all' (users 0-49) or specific IDs (e.g., 1 2 5).

  Cases: Accepts 'all' (cases 1-7) or specific cases (e.g., 1 3).

  Tools: Accepts 'all', 'IMU' (Tool 0), or 'Samsung' (Tool 1).

  IDs: Specifies sensor IDs (e.g., IMU 0 1 2 3 or Samsung 0).

variable_selection_numpy(dataset, users, cases, tools, ids) returns a tuple of concatenated NumPy arrays containing the requested data block alongside its corresponding labels: (data, user_labels, case_labels, tool_labels, ids).

Data Visualisation:

The repository includes a dedicated visualisation script (data_visualisation.py) to easily inspect the synchronized IMU streams using Matplotlib. By default, it is configured to evaluate a specific time window (start and end frames) for a specific user and case.

The script generates a comprehensive 3x3 grid plot that provides a joint view of the 3D components (X, Y, and Z axes) for:

  Gravity (g_x, g_y, g_z)

  Linear Acceleration (a_x, a_y, a_z)

  Angular Velocity (w_x, w_y, w_z)

By default, the script compares the left and right ankle sensors (IMU 1 and IMU 3) within the same axes to easily observe gait symmetry and synchronisation.

REFERENCE
=============
Should you use this dataset in your publication please cite the following:

Moca Dataset can be also downloaded at <a href=>Mendeley Data</a>. -->

<p align="center">
  <img src="Figures/logo.png" width="550" title="hover text">
</p>

## The MARCH dataset: Multi-modal learning for gait-based human analysis and authentication


### Description and motivations

The MARCH dataset is a comprehensive and rich multimodal dataset composed of inertial and video data. This dataset aims to provide a rich and diverse description of different walking patterns. It will be rich because it includes a large number of individuals of various ages and genders. It will be diverse as it incorporates data from multiple devices, and various clothing styles, ensuring an appropriate level of variability. 

The dataset consists in 50 gender-balanced participants (26 males and 24 females), of age 26.8± 2.9 performing 7 different walks on a treadmill of 5 minutes each in indoor environment. During the first two trials, the treadmill velocity was fixed at 2 km/h. In the third and fourth trials, participants chose a comfortable walking speed. For the fifth and sixth trials, the speed remained user-selected; however, a one-kilogram weight was fastened to the participant's left ankle to simulate an injury. The seventh and final trial followed a pre-programmed speed profile. Every 30 seconds, the velocity shifted between a minimum of 2 km/h and a maximum of 5 km/h according to the following sequence (in km/h): (2,4,3,4,3,5,4,2,5,3).

Additionally, all even-numbered trials were conducted barefoot, while odd-numbered trials were performed with shoes. These conditions are summarised in the following Table.

<p align="center">
  <img src="Figures/data.png" width="550" title="hover text">
</p>

Each user worn five sensors, four IMUs and one smartphone.  Two IMUs were secured to the exterior of both ankles, while the remaining two were fastened to the exterior middle section of both thighs; all were held in place using Velcro straps. When the participant stood in a stationary position, the IMUs were oriented such that the x-axis was parallel to the leg (pointing downward), and the z-axis was parallel to the ground, pointing toward the inner part of the body. The y-axis was oriented according to the left-hand rule.

The Samsung smartphone was placed in the back-left pocket of the trousers with the y-axis oriented perpendicularly to the ground, the z-axis pointing toward the body, and the x-axis oriented according to the right-hand rule. 

The figure illustrates the IMU positions (red circles) and the Samsung smartphone placement (yellow circle)

<p align="center">
  <img src="Figures/position_cropped.png" width="550" title="hover text">
</p>

Additionally, we collected timestamps of all sensors simplifying the synchronisation across all devises. In total we collected 29.16 hours of data per sensor.

### Getting started

Clone the repository and install the dependencies (Python 3.8+ recommended):

```bash
git clone https://github.com/Malga-Vision/MARCH.git
cd MARCH
pip install -r requirements.txt
```

The raw data is shipped under `Data/` with the directory structure
`Data/user_<id>_sync/case_<n>/<IMUs|Samsung>/<sensor>.csv`.

**Load data into NumPy arrays.** Run from the `Functions/Data_loading/` directory
(the script uses a relative path to `../../Data/`):

```bash
cd Functions/Data_loading
python data_upload_numpy.py
```

The script will interactively prompt for the selection (users, cases, tool,
sensor IDs). Example session that loads IMU 1 and IMU 3 of user 0, case 1:

```
Inserire user (or 'all'): 0
Inserire case (or 'all'): 1
Inserire tool (all, IMU, Samsung): IMU
Quali IMUs (es. 0 1 2 3): 1 3
```

To bypass the prompts, you can also call `get_selection_config(...)` and
`variable_selection_numpy(...)` programmatically with the same arguments.

**Visualise IMU signals.** Run from the `Functions/Data_visualisation/`
directory; the script reads `user_00_sync/case_1` from `Data/` and writes
`plot.png` next to the script:

```bash
cd Functions/Data_visualisation
python data_visualisation.py
```

### Technical information: NumPy Data Structure

The User_Case_Dataset_NumPy class parses the dataset's directory tree (root_dir / user / case / instrument / data_file) and converts the raw CSV files into structured NumPy arrays.

Calling the dataset via its index (dataset[idx]) returns a tuple containing the sensor data matrix alongside its four corresponding identifying labels: (data_array, user_label, case_label, tool_label, data_id).

1. The Data Matrix (data_array)
Each returned data_array is a 2D NumPy array where rows represent continuous time samples and the 11 columns contain the specific kinematic values. The columns are structured exactly as follows:

    Col 0: timestamp_ns (System timestamp in nanoseconds)

    Col 1: wx (Angular velocity X)

    Col 2: wy (Angular velocity Y)

    Col 3: wz (Angular velocity Z)

    Col 4: ax (Linear acceleration X)

    Col 5: ay (Linear acceleration Y)

    Col 6: az (Linear acceleration Z)

    Col 7: gx (Gravity X)

    Col 8: gy (Gravity Y)

    Col 9: gz (Gravity Z)

    Col 10: time_ms_loc (Local time in milliseconds, used for synchronized plotting)

2. Label Encodings
To facilitate segmentation and machine learning training, the data is paired with integer-encoded labels. These guarantee you always know the exact context of the data_array:

    user_label [0 to n]: Identifies the specific subject performing the trial.

    case_label [1 to 7]: Identifies the specific gait scenario or testing condition being executed.

    tool_label [0 or 1]: Identifies the hardware system used for the capture:

      0 = Wearable IMUs

      1 = Smartphone (Sensor Logger App)

    data_id: Specifies the exact spatial location or identifier of the sensor:

      If tool_label == 0 (IMUs): Evaluates to 0, 1, 2, or 3 (imu_0 through imu_3).

      If tool_label == 1 (Smartphone): Evaluates to 0.

### Available functions
Loading and visualisation scripts allow users to access, filter, and plot the MARCH inertial data.

The data loading functions (get_selection_config and variable_selection_numpy) allow the user to load specific subsets of the MARCH dataset into easy-to-use NumPy arrays. You can filter the data by users, cases, tools (IMU vs. Smartphone), and specific sensor IDs.

Syntax & Data Loading:

get_selection_config(user_input, case_input, tool_input, id_input) parses your selection criteria. If arguments are omitted, it prompts the user for inputs interactively via the console.

  Users: Accepts 'all' (users 0-49) or specific IDs (e.g., 1 2 5).

  Cases: Accepts 'all' (cases 1-7) or specific cases (e.g., 1 3).

  Tools: Accepts 'all', 'IMU' (Tool 0), or 'Samsung' (Tool 1).

  IDs: Specifies sensor IDs (e.g., IMU 0 1 2 3 or Samsung 0).

variable_selection_numpy(dataset, users, cases, tools, ids) returns a tuple of concatenated NumPy arrays containing the requested data block alongside its corresponding labels: (data, user_labels, case_labels, tool_labels, ids).

Data Visualisation:

The repository includes a dedicated visualisation script (data_visualisation.py) to easily inspect the synchronized IMU streams using Matplotlib. By default, it is configured to evaluate a specific time window (start and end frames) for a specific user and case.

The script generates a comprehensive 3x3 grid plot that provides a joint view of the 3D components (X, Y, and Z axes) for:

  Gravity (g_x, g_y, g_z)

  Linear Acceleration (a_x, a_y, a_z)

  Angular Velocity (w_x, w_y, w_z)

By default, the script compares the left and right ankle sensors (IMU 1 and IMU 3) within the same axes to easily observe gait symmetry and synchronisation.

REFERENCE
=============
Should you use this dataset in your publication please cite the following:

Moca Dataset can be also downloaded at <a href=>Mendeley Data</a>.