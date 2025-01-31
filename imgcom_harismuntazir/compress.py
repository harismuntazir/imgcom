#!/usr/bin/env python3

import os
import sys
from PIL import Image

def compress_image(image_path, quality, max_size):
    image = Image.open(image_path).convert("RGB")
    output_path = "out_" + os.path.basename(image_path)
    
    current_quality = quality
    temp_output = "temp_" + output_path
    
    # First, try reducing quality without resizing
    while current_quality >= 10:
        image.save(temp_output, "JPEG", quality=current_quality)
        if os.path.getsize(temp_output) / 1024 <= max_size:
            os.replace(temp_output, output_path)
            return output_path
        current_quality -= 5
    
    # If quality reduction isn't enough, start resizing with minimum quality
    current_quality = 10
    resized_image = image.copy()
    while resized_image.size[0] > 1:
        # Calculate new dimensions as 90% of current size, cast to integers
        new_width = int(resized_image.size[0] * 0.9)
        new_height = int(resized_image.size[1] * 0.9)
        resized_image.thumbnail((new_width, new_height))
        resized_image.save(temp_output, "JPEG", quality=current_quality)
        if os.path.getsize(temp_output) / 1024 <= max_size:
            os.replace(temp_output, output_path)
            return output_path
    
    # Cleanup temp file if loop exited without saving
    if os.path.exists(temp_output):
        os.remove(temp_output)
    resized_image.save(output_path, "JPEG", quality=current_quality)
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: imgcom <image_file> [--version] [--about]")
        sys.exit(1)

    if sys.argv[1] == "--version":
        print("Installed imgcom Version 1.5.0")
        sys.exit(0)
    
    if sys.argv[1] == "--about":
        print("imgcom - A command-line tool to compress images.")
        print("Author: Haris Muntazir")
        print("GitHub: https://github.com/harismuntazir")
        sys.exit(0)

    file_name = sys.argv[1]
    compress_upto = int(input("Enter the compression quality (1-100): "))
    if compress_upto < 1 or compress_upto > 100:
        print("Quality must be between 1 and 100.")
        sys.exit(1)
    max_size = float(input("Enter the desired maximum size in KB: "))
    
    output_file = compress_image(file_name, compress_upto, max_size)
    size = os.path.getsize(output_file) / 1024
    print(f"The output file size is: {size:.2f} KB")
    print("The compression completed successfully.")

if __name__ == "__main__":
    main()
