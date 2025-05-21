import os
import requests
import json
from PIL import Image
from io import BytesIO
import hashlib
from .utils import setup_directories, convert_to_rgb

def optimize_url_images(url_file_path, quality=80):
    """
    Reads image URLs from a JSON file, downloads them, optimizes them, and saves as WebP files
    in the 'out' directory.

    Args:
        url_file_path (str): Path to the JSON file containing image URLs
        quality (int): WebP quality (0-100), default 80
    """
    # Setup directories
    _, output_directory = setup_directories()

    # Read URLs from JSON file
    try:
        with open(url_file_path, 'r') as file:
            # Skip comment lines that start with //
            content = "\n".join([line for line in file if not line.strip().startswith("//")])
            url_data = json.loads(content)
    except Exception as e:
        print(f"Error reading URL JSON file: {e}")
        return

    if not url_data:
        print("No URLs found in the JSON file.")
        return

    # Process each URL entry
    for item in url_data:
        try:
            url = item.get("url")
            custom_filename = item.get("filename")

            if not url:
                print("Skipping entry with no URL")
                continue

            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Use custom filename if provided, otherwise extract from URL
            if custom_filename:
                name_without_ext = custom_filename
            else:
                # Generate a filename from URL if no custom filename is available
                url_filename = url.split('/')[-1].split('?')[0]  # Try to extract filename from URL

                # If no valid filename, use a hash of the URL
                if not url_filename or '.' not in url_filename:
                    url_hash = hashlib.md5(url.encode()).hexdigest()
                    url_filename = f"image_{url_hash}"

                # Get name without extension
                name_without_ext = os.path.splitext(url_filename)[0]

            # Open the image from the response content
            with Image.open(BytesIO(response.content)) as img:
                # Convert to RGB if needed
                img = convert_to_rgb(img)

                # Output path for WebP file
                output_path = os.path.join(output_directory, f"{name_without_ext}.webp")

                # Save as WebP
                img.save(output_path, 'WEBP', quality=quality)

                print(f"Optimized from URL: {url} -> {os.path.basename(output_path)}")

        except Exception as e:
            print(f"Error processing URL {url if 'url' in locals() else 'unknown'}: {e}")