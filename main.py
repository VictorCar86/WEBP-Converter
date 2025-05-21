import os
import sys
from src.local_optimizer import optimize_local_images
from src.url_optimizer import optimize_url_images

def main():
    # Get quality from command line if provided
    quality = int(sys.argv[1]) if len(sys.argv) > 1 else 80

    # Process local images
    print("Processing local images...")
    optimize_local_images(quality)

    # Process images from URLs
    print("\nProcessing images from URLs...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    url_file_path = os.path.join(base_dir, "input_images_url.jsonc")
    if os.path.exists(url_file_path):
        optimize_url_images(url_file_path, quality)
    else:
        print(f"URL file not found: {url_file_path}")

    print("\nImage optimization complete. Check the 'out' folder for results.")

if __name__ == "__main__":
    main()