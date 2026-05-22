import numpy as np

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
        c = dataset.case_labels[idx] + 1 
        t = dataset.tool_labels[idx]
        d_id = dataset.data_ids[idx]

        # 3. Check criteria
        if (u in user_set and 
            c in case_set and 
            t in tool_set and 
            d_id in ids_set):
            
            
            data, _, _, _, _ = dataset[idx] 
            
            n_samples = data.shape[0]
            
           
            all_data.append(data)
            
            
            all_user.append(np.full((n_samples,), u, dtype=np.int64))
            all_case.append(np.full((n_samples,), c, dtype=np.int64))
            all_tool.append(np.full((n_samples,), t, dtype=np.int64))
            all_ids.append(np.full((n_samples,), d_id, dtype=np.int64))

    # 5. Handle empty selection case to avoid errors
    if not all_data:
        print("Warning: No data matched the selection criteria.")
        return None, None, None, None, None

    # 6. Concatenate all segments (Equivalent to torch.cat)
    return (
        np.concatenate(all_data, axis=0), 
        np.concatenate(all_user, axis=0), 
        np.concatenate(all_case, axis=0), 
        np.concatenate(all_tool, axis=0), 
        np.concatenate(all_ids, axis=0)
    )

def get_selection_config(user_input = None, case_input = None, tool_input = None, id_input = None):
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
        - 'all': selects all tools (IMUs, Samsung).
        - 'IMU': selects tool 0. Requires 'id_input' to specify which IMUs (0, 1, 2, 3).
        - 'Samsung': selects tool 1 and default ID 0.
        
    id_input : str or None
        - Only used if tool_input is 'IMU'.
        - Space-separated numbers (e.g., "1 2") for specific IMU IDs.

    Returns:
    --------
    tuple (users, cases, tools, ids)
        Lists of integers representing the selected configuration.
    """

    # --- 1. Handle Users ---
    if user_input is None:
        user_input = input("Inserire user (or 'all'): ").strip()

    if user_input == "all":
        users = list(range(50))
    else:
        # Handle simple integer or list input safely
        if isinstance(user_input, list): 
            users = user_input
        else:
            users = [int(x) for x in str(user_input).split()]
    print(f"Users selected: {users}")

    # --- 2. Handle Cases ---
    if case_input is None:
        case_input = input("Inserire case (or 'all'): ").strip()

    if case_input == "all":
        cases = list(range(1, 8))
    else:
        if isinstance(case_input, list):
            cases = case_input
        else:
            cases = [int(x) for x in str(case_input).split()]
    print(f"Cases selected: {cases}")

    # --- 3. Handle Tools & IDs ---
    if tool_input is None:
        tool_input = input("Inserire tool (all, IMU, Samsung): ").strip()

    tools = []
    ids = []

    if tool_input == "all":
        tools = [0, 1]
        ids = [0, 1, 2, 3] # Adjust if Samsung doesn't have 4 IDs
        
    elif tool_input == "IMU":
        tools = [0]
        
        # Check if ID input was provided, otherwise ask
        if id_input is None:
            id_input = input("Quali IMUs (es. 0 1 2 3): ").strip()
            
        if isinstance(id_input, list):
            ids = id_input
        else:
            ids = [int(x) for x in str(id_input).split()]
            
    elif tool_input == "Samsung":
        tools = [1]
        ids = [0] # Assuming Samsung only has ID 0

    print(f"Tools: {tools}, IDs: {ids}")

    return users, cases, tools, ids