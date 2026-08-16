from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py <image>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    output_path = input_path.with_name("source-prepped.png")

    # Load image and remove the background.
    image = Image.open(input_path).convert("RGBA")
    foreground = remove(image).convert("RGBA")

    # Create a pure white background.
    white = Image.new("RGBA", foreground.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white, foreground).convert("RGB")

    # Convert to grayscale.
    gray = np.array(composited)
    gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)

    # Improve local contrast using CLAHE.
    clahe = cv2.createCLAHE(
        clipLimit=2.2,
        tileGridSize=(8, 8)
    )
    enhanced = clahe.apply(gray)

    # Keep the output as a clean PNG.
    Image.fromarray(enhanced).save(output_path)

    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
