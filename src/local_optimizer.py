import os
import glob
from PIL import Image
from .utils import setup_directories, convert_to_rgb

def optimize_local_images(quality=80):
    """
    Reads all images from 'input_images' directory, optimizes them, and saves as WebP files
    in the 'out' directory.

    Args:
        quality (int): WebP quality (0-100), default 80
    """
    # Setup directories
    input_directory, output_directory = setup_directories()

    # Check if input directory exists
    if not os.path.isdir(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist.")
        return

    # Get all image files (common formats)
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_directory, ext)))
        # Include uppercase extensions
        image_files.extend(glob.glob(os.path.join(input_directory, ext.upper())))

    if not image_files:
        print(f"No image files found in '{input_directory}'.")
        return

    # Process each image
    for image_path in image_files:
        try:
            # Get filename without extension
            filename = os.path.basename(image_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Open and optimize the image
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                img = convert_to_rgb(img)

                # Output path for WebP file
                output_path = os.path.join(output_directory, f"{name_without_ext}.webp")

                # Save as WebP
                img.save(output_path, 'WEBP', quality=quality)

                print(f"Optimized: {filename} -> {os.path.basename(output_path)}")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")