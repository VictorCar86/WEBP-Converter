import os
import requests
import json
from PIL import Image
from io import BytesIO
import hashlib
from .utils import setup_directories, convert_to_rgb

def optimize_url_images(url_file_path, quality=80, keep_original=False):
    """
    Reads image URLs from a JSON file, downloads them, optimizes them, and saves as WebP files
    in the 'output' directory. Optionally saves original downloaded files.

    Args:
        url_file_path (str): Path to the JSON file containing image URLs
        quality (int): WebP quality (0-100), default 80
        keep_original (bool): If True, saves a copy of the original downloaded image.
    """
    # Setup directories
    _, output_directory = setup_directories()
    originals_url_dir = os.path.join(output_directory, "originals_from_url")

    if keep_original:
        os.makedirs(originals_url_dir, exist_ok=True)

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
            original_filename_with_ext = ""
            if custom_filename:
                name_without_ext = custom_filename
                # Try to guess extension from URL if custom_filename doesn't have one
                # This is a simple guess; Content-Type header would be more robust
                url_path_part = url.split('?')[0]
                if '.' in url_path_part.split('/')[-1]:
                    original_ext = os.path.splitext(url_path_part.split('/')[-1])[1]
                    original_filename_with_ext = f"{name_without_ext}{original_ext}"
                else: # fallback if no extension in URL
                    original_filename_with_ext = name_without_ext # No extension, will save as is
            else:
                # Generate a filename from URL if no custom filename is available
                url_filename_part = url.split('/')[-1].split('?')[0]

                if not url_filename_part or '.' not in url_filename_part:
                    url_hash = hashlib.md5(url.encode()).hexdigest()
                    # Attempt to get extension from content-type if possible, otherwise default
                    content_type = response.headers.get('content-type')
                    ext_from_content_type = ""
                    if content_type and '/' in content_type:
                        mime_subtype = content_type.split('/')[1]
                        if mime_subtype == 'jpeg': ext_from_content_type = '.jpg'
                        elif mime_subtype in ['png', 'gif', 'bmp', 'webp', 'tiff']:
                             ext_from_content_type = f'.{mime_subtype}'

                    original_filename_with_ext = f"image_{url_hash}{ext_from_content_type}"
                    name_without_ext = os.path.splitext(original_filename_with_ext)[0]
                else:
                    original_filename_with_ext = url_filename_part
                    name_without_ext = os.path.splitext(url_filename_part)[0]
            
            if not original_filename_with_ext: # Ensure there's a filename
                original_filename_with_ext = name_without_ext


            # Save original image if requested
            if keep_original:
                original_save_path = os.path.join(originals_url_dir, original_filename_with_ext)
                try:
                    with open(original_save_path, 'wb') as f_orig:
                        f_orig.write(response.content)
                    print(f"Saved original: {url} -> {original_save_path}")
                except Exception as e_save_orig:
                    print(f"Error saving original for {url}: {e_save_orig}")


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