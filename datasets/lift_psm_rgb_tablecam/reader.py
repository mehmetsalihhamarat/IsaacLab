import h5py

# Load your dataset
dataset_path = "dataset.hdf5"  # Replace with the path to your dataset

with h5py.File(dataset_path, "r") as f:
    # Access the 'data' group and 'demo_0' subgroup
    data_group = f["data"]
    demo_group = data_group["demo_0"]  # Access 'demo_0' within 'data'
    
    # Print keys inside 'demo_0' for clarity
    print("\nKeys inside 'demo_0':")
    print(list(demo_group.keys()))

    # Explore the content of 'obs' group
    if 'obs' in demo_group:
        obs_group = demo_group['obs']
        print("\n'obs' group contents:")
        print(list(obs_group.keys()))  # Print the subgroups or datasets inside 'obs'
        
        # Check if 'table_cam' is a dataset and print its content
        if 'table_cam' in obs_group:
            table_cam_data = obs_group['table_cam']
            if isinstance(table_cam_data, h5py.Dataset):
                print("\n'obs/table_cam' content:")
                print(table_cam_data[:])  # Print the content of 'table_cam'

    # Explore the content of 'states' group
    if 'states' in demo_group:
        states_group = demo_group['states']
        print("\n'states' group contents:")
        print(list(states_group.keys()))  # Print the subgroups or datasets inside 'states'
        
        # Check if 'articulation' and 'rigid_object' are datasets and print their content
        if 'articulation' in states_group:
            articulation_data = states_group['articulation']
            if isinstance(articulation_data, h5py.Dataset):
                print("\n'rigid_object' content:")
                print(articulation_data[:])  # Print the content of 'articulation'
        
        if 'rigid_object' in states_group:
            rigid_object_data = states_group['rigid_object']
            if isinstance(rigid_object_data, h5py.Dataset):
                print("\n'rigid_object' content:")
                print(rigid_object_data[:])  # Print the content of 'rigid_object'
