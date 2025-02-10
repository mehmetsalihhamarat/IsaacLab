import h5py
import numpy as np
import matplotlib.pyplot as plt

# Load your dataset
dataset_path = "dataset.hdf5"  # Replace with your actual dataset path

with h5py.File(dataset_path, "r") as f:
    # Access 'table_cam' inside 'obs' in 'demo_0'
    table_cam_data = f["data"]["demo_0"]["obs"]["table_cam"]
    wrist_cam_data = f["data"]["demo_0"]["obs"]["wrist_cam"]

    # Convert to numpy array
    img_array = np.array(table_cam_data)
    img_array_1 = np.array(wrist_cam_data)

    # Print image shape for debugging
    print(f"Table original image shape: {img_array.shape}")
    print(f"Wrist original image shape: {img_array_1.shape}")

    # If the image is stored as (N, H, W, C), pick first frame
    if len(img_array.shape) == 4:
        img_array = img_array[0]
    
    if len(img_array_1.shape) == 4:
        img_array_1 = img_array_1[0]

    # If stored as (C, H, W), transpose to (H, W, C)
    if img_array.shape[0] in [1, 3] and img_array.shape[1] > 10:  # Heuristic check
        img_array = np.transpose(img_array, (1, 2, 0))
    
    if img_array_1.shape[0] in [1, 3] and img_array_1.shape[1] > 10:  # Heuristic check
        img_array_1 = np.transpose(img_array_1, (1, 2, 0))

    # Normalize if values are not in [0,1] range
    if img_array.max() > 1:
        img_array = img_array / 255.0
    
    if img_array_1.max() > 1:
        img_array_1 = img_array_1 / 255.0

    # Resize for better visualization (if needed)
    from skimage.transform import resize
    upscale_factor = 4  # Increase resolution
    img_array = resize(img_array, (img_array.shape[0] * upscale_factor, img_array.shape[1] * upscale_factor), anti_aliasing=True)
    img_array_1 = resize(img_array_1, (img_array_1.shape[0] * upscale_factor, img_array_1.shape[1] * upscale_factor), anti_aliasing=True)

    # Display the image
    plt.figure(figsize=(8, 8))
    
    plt.subplot(1,2,1)
    plt.imshow(img_array)
    plt.axis("off")
    plt.title("High-Resolution 'table_cam' Image")

    plt.subplot(1,2,2)
    plt.imshow(img_array_1)
    plt.axis("off")
    plt.title("High-Resolution 'wrist_cam' Image")

    plt.show()


