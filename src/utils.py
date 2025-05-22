import os
from PIL import Image

def setup_directories():
    """
    Sets up input and output directories.

    Returns:
        tuple: (input_directory, output_directory)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_directory = os.path.join(base_dir, "input")
    output_directory = os.path.join(base_dir, "output")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    return input_directory, output_directory

def convert_to_rgb(img):
    """
    Converts an image to RGB format, handling transparency if needed.

    Args:
        img (PIL.Image): The image to convert

    Returns:
        PIL.Image: The converted image
    """
    if img.mode == 'RGBA':
        # If image has transparency, add a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    elif img.mode != 'RGB':
        return img.convert('RGB')
    return img