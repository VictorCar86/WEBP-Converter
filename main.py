import os
from src.local_optimizer import optimize_local_images
from src.url_optimizer import optimize_url_images
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Optimiza imágenes locales y desde URLs a formato WebP."
    )
    parser.add_argument(
        "quality",
        type=int,
        nargs="?",  # Makes the argument optional
        default=80,
        help="Calidad de compresión para WebP (0-100, por defecto: 80). "
             "Este argumento es posicional.",
    )
    parser.add_argument(
        "--flat_output",
        action="store_true",  # Si está presente, args.flat_output será True
        help="Guarda todas las imágenes locales procesadas directamente en la raíz de la carpeta 'output', "
             "sin preservar la estructura de subdirectorios de 'input'. "
             "Por defecto, se preserva la estructura.",
    )
    args = parser.parse_args()

    quality = args.quality
    # Si --flat_output está presente, preserve_structure será False.
    # De lo contrario (comportamiento por defecto), preserve_structure será True.
    preserve_structure_for_local = not args.flat_output

    # Process local images
    print("Processing local images...")
    optimize_local_images(quality, preserve_structure=preserve_structure_for_local)

    # Process images from URLs
    print("\nProcessing images from URLs...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    url_file_path = os.path.join(base_dir, "input_url.jsonc")
    if os.path.exists(url_file_path):
        optimize_url_images(url_file_path, quality)
    else:
        print(f"URL file not found: {url_file_path}")

    print("\nImage optimization complete. Check the 'output' folder for results.")

if __name__ == "__main__":
    main()