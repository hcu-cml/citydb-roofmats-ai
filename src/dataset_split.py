import os
import shutil
import random

def split_dataset(image_dir, annotation_dir, output_dir, train_size=0.7, val_size=0.15, test_size=0.15):
    # Ensure sizes sum up to 1
    assert train_size + val_size + test_size == 1, "Sizes must sum to 1."
    
    # Create output directories
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'gt'), exist_ok=True)
    
    # Get all image files
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('png', 'jpg', 'jpeg', 'tif'))]
    random.shuffle(image_files)
    
    # Compute split indices
    total_images = len(image_files)
    train_end = int(total_images * train_size)
    val_end = train_end + int(total_images * val_size)
    
    # Split dataset
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]
    
    # Move files to respective directories
    for file in train_files:
        shutil.move(os.path.join(image_dir, file), os.path.join(output_dir, 'train', 'images', file))
        shutil.move(os.path.join(annotation_dir, file), os.path.join(output_dir, 'train', 'gt', file))
    for file in val_files:
        shutil.move(os.path.join(image_dir, file), os.path.join(output_dir, 'val', 'images', file))
        shutil.move(os.path.join(annotation_dir, file), os.path.join(output_dir, 'val', 'gt', file))
    for file in test_files:
        shutil.move(os.path.join(image_dir, file), os.path.join(output_dir, 'test', 'images', file))
        shutil.move(os.path.join(annotation_dir, file), os.path.join(output_dir, 'test', 'gt', file))
    
    print(f"Dataset split complete: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test.")

# Run program
split_dataset("./reference", "./annotations", "./dataset", train_size=0.7, val_size=0.15, test_size=0.15)
