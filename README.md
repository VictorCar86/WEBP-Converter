# WebP Converter

A Python utility for optimizing images from both local directories and URLs, converting them to the efficient WebP format.

## Overview

Image Optimizer is a command-line tool that:
- Processes images from a local directory (`input`)
- Downloads and processes images from URLs specified in a JSON file
- Converts all images to WebP format with customizable quality settings
- Handles various image formats (JPG, JPEG, PNG, BMP, GIF, TIFF)
- Properly handles transparency in images
- Supports preserving directory structure or flat output organization

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/image_optimizer.git
cd image_optimizer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Preparing Input

1. **Local Images**: Place your images in the `input` directory (will be created automatically if it doesn't exist)

2. **URL Images**: Edit the `input_url.jsonc` file with your image URLs:
```json
[
  {
    "filename": "example_image",
    "url": "https://example.com/image.jpg"
  }
]
```

### Running the Optimizer

Run the optimizer with default settings (80% quality):
```bash
python main.py
```

Specify a custom quality level (0-100):
```bash
python main.py 90
```

Use flat output structure (all files in output root):
```bash
python main.py --flat_output
```

Combine quality and flat output:
```bash
python main.py 90 --flat_output
```

## Features

- **WebP Conversion**: All images are converted to the efficient WebP format
- **Quality Control**: Adjust compression quality via command-line parameter
- **Transparency Handling**: Properly handles RGBA images with transparency
- **Flexible Input**: Process images from both local files and remote URLs
- **Error Handling**: Robust error handling for both local and remote images
- **Directory Structure Options**: Choose between preserving directory structure or flat output

## Requirements

- Python 3.6+
- Pillow 11.1.0
- Requests 2.32.3

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.