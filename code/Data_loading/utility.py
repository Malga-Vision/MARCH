import numpy as np


VALID_USERS = range(50)
VALID_CASES = range(1, 8)
VALID_IMU_IDS = range(4)
IMU_NAME_TO_ID = {
    "RT": 0,
    "RA": 1,
    "LT": 2,
    "LA": 3,
}


def variable_selection_numpy(dataset, user_selected, case_selected, tool_selected, ids_selected):
    user_set = set(user_selected)
    case_set = set(case_selected)
    tool_set = set(tool_selected)
    ids_set = set(ids_selected)

    all_data = []
    all_user = []
    all_case = []
    all_tool = []
    all_ids = []

    for idx in range(len(dataset)):
        u = dataset.user_labels[idx]
        c = dataset.case_labels[idx]
        t = dataset.tool_labels[idx]
        d_id = dataset.data_ids[idx]

        if (
            u in user_set
            and c in case_set
            and t in tool_set
            and d_id in ids_set
        ):
            data, _, _, _, _ = dataset[idx]
            n_samples = data.shape[0]

            all_data.append(data)
            all_user.append(np.full((n_samples,), u, dtype=np.int64))
            all_case.append(np.full((n_samples,), c, dtype=np.int64))
            all_tool.append(np.full((n_samples,), t, dtype=np.int64))
            all_ids.append(np.full((n_samples,), d_id, dtype=np.int64))

    if not all_data:
        print("Warning: No data matched the selection criteria.")
        return None, None, None, None, None

    return (
        np.concatenate(all_data, axis=0),
        np.concatenate(all_user, axis=0),
        np.concatenate(all_case, axis=0),
        np.concatenate(all_tool, axis=0),
        np.concatenate(all_ids, axis=0)
    )


def get_selection_config(user_input=None, case_input=None, tool_input=None, id_input=None):
    """
    Parses selection criteria for Users, Cases, Tools, and IDs.
    
    If arguments are not provided (None), the function will prompt the user
    for input via the console.

    Parameters:
    -----------
    user_input : str or None
        - 'all': selects users 0 to 49.
        - Space-separated numbers (e.g., "1 2 5"): selects specific users.

    case_input : str or None
        - 'all': selects cases 1 to 7.
        - Space-separated numbers (e.g., "1 3"): selects specific cases.

    tool_input : str or None
        - 'all': selects all tools (IMUs, Smartphone).
        - 'IMU': selects tool 0. Requires 'id_input' to specify which IMUs (RT, RA, LT, LA).
        - 'Smartphone': selects tool 1 and default ID 0.

    id_input : str or None
        - Only used if tool_input is 'IMU'.
        - Space-separated names (e.g., "RA LA") for specific IMUs.

    Returns:
    --------
    tuple (users, cases, tools, ids)
        Lists of integers representing the selected configuration.
    """

    if user_input is None:
        user_input = input("Inserire user (or 'all'): ").strip()

    if _is_all(user_input):
        users = list(VALID_USERS)
    else:
        users = _parse_int_list(user_input, "users", VALID_USERS)
    print(f"Users selected: {users}")

    if case_input is None:
        case_input = input("Inserire case (or 'all'): ").strip()

    if _is_all(case_input):
        cases = list(VALID_CASES)
    else:
        cases = _parse_int_list(case_input, "cases", VALID_CASES)
    print(f"Cases selected: {cases}")

    if tool_input is None:
        tool_input = input("Inserire tool (all, IMU, Smartphone): ").strip()

    tool = str(tool_input).strip().lower()
    if tool == "all":
        tools = [0, 1]
        ids = list(VALID_IMU_IDS)
    elif tool in {"imu", "imus"}:
        tools = [0]

        if id_input is None:
            id_input = input("Quali IMUs (es. RT RA LT LA): ").strip()
        if _is_all(id_input):
            ids = list(VALID_IMU_IDS)
        else:
            ids = _parse_imu_names(id_input)
    elif tool in {"smartphone", "phone"}:
        tools = [1]
        ids = [0]
    else:
        raise ValueError("Invalid tool. Expected 'all', 'IMU', or 'Smartphone'.")

    print(f"Tools: {tools}, IDs: {ids}")

    return users, cases, tools, ids


def _is_all(value):
    return isinstance(value, str) and value.strip().lower() == "all"


def _parse_imu_names(value):
    if isinstance(value, str):
        names = value.replace(",", " ").split()
    elif isinstance(value, (list, tuple, set)):
        names = [str(item) for item in value]
    else:
        names = [str(value)]

    if not names:
        raise ValueError("No IMUs selected.")

    normalized_names = [name.strip().upper() for name in names]
    invalid = [name for name in normalized_names if name not in IMU_NAME_TO_ID]
    if invalid:
        valid_names = ", ".join(IMU_NAME_TO_ID)
        raise ValueError(
            f"Invalid IMU names: {invalid}. Expected one or more of: {valid_names}."
        )

    return [IMU_NAME_TO_ID[name] for name in normalized_names]


def _parse_int_list(value, label, valid_values):
    valid_values = list(valid_values)
    valid_set = set(valid_values)

    if isinstance(value, (int, np.integer)):
        parsed = [int(value)]
    elif isinstance(value, (list, tuple, set)):
        parsed = [int(item) for item in value]
    else:
        tokens = str(value).replace(",", " ").split()
        if not tokens:
            raise ValueError(f"No {label} selected.")
        parsed = [int(token) for token in tokens]

    invalid = [item for item in parsed if item not in valid_set]
    if invalid:
        valid_range = f"{min(valid_values)}-{max(valid_values)}"
        raise ValueError(f"Invalid {label}: {invalid}. Expected values in {valid_range}.")

    return parsed
