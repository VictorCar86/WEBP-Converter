import os
from PIL import Image
from .utils import setup_directories, convert_to_rgb

def optimize_local_images(quality=80, preserve_structure=True): # Added preserve_structure, default True
    """
    Reads images from 'input' directory (including subdirectories),
    optimizes them, and saves as WebP files in the 'output' directory.

    Args:
        quality (int): WebP quality (0-100), default 80
        preserve_structure (bool): If True, replicates the subdirectory structure
                                   from 'input' into 'output'. If False,
                                   saves all images to the root of 'output'.
                                   Default is True.
    """
    # Setup directories
    input_directory, output_directory = setup_directories()

    # Check if input directory exists
    if not os.path.isdir(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist.")
        return

    image_files_processed = 0
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.lower().endswith(valid_extensions):
                image_path = os.path.join(root, filename)
                try:
                    name_without_ext = os.path.splitext(filename)[0]

                    if preserve_structure:
                        # Calculate relative path from input_directory
                        relative_dir = os.path.relpath(root, input_directory)
                        # Construct target output directory
                        current_output_dir = os.path.join(output_directory, relative_dir)
                        # Create subdirectory in 'output' if it doesn't exist
                        if relative_dir and relative_dir != ".": # Avoid joining "." if file is in root of input
                            os.makedirs(current_output_dir, exist_ok=True)
                        else: # file is in the root of input, output_dir is already correct
                            current_output_dir = output_directory
                        
                        output_path = os.path.join(current_output_dir, f"{name_without_ext}.webp")
                    else:
                        # Save directly to the root of output_directory
                        output_path = os.path.join(output_directory, f"{name_without_ext}.webp")

                    # Open and optimize the image
                    with Image.open(image_path) as img:
                        # Convert to RGB if needed
                        img = convert_to_rgb(img)
                        # Save as WebP
                        img.save(output_path, 'WEBP', quality=quality)
                        print(f"Optimized: {image_path} -> {output_path}")
                        image_files_processed += 1

                except Exception as e:
                    print(f"Error processing {image_path}: {e}")

    if image_files_processed == 0:
        print(f"No image files found in '{input_directory}' or its subdirectories.")