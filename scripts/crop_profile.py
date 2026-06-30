"""Crop the horizontal Banff photo into a vertical portrait focused on the person."""
from PIL import Image
import sys

SRC = "images/Bio_Photo_Banff.jpg"
OUT = sys.argv[1] if len(sys.argv) > 1 else "images/_crop_preview.jpg"

# Crop box (left, top, right, bottom) in the 1920x1280 source.
# Person stands right-of-center; this frames head-to-hips, vertical ~3:4.
LEFT, TOP, RIGHT, BOTTOM = 892, 360, 1529, 1210

img = Image.open(SRC)
crop = img.crop((LEFT, TOP, RIGHT, BOTTOM))
crop.save(OUT, quality=92)
print(f"saved {OUT} size={crop.size} aspect={crop.size[0]/crop.size[1]:.3f}")
