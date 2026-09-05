import os
from PIL import Image, ImageOps

MIN_SIZE = 300
MAX_SIZE = 4000


def validate_image(path):
    """
    Checks if an image is safe to process.
    Returns (image_object, error_message).
    If successful, error_message is None.
    If failed, image_object is None.
    """

    if not os.path.exists(path):
        return None, "File not found"

    if os.path.getsize(path) == 0:
        return None, "File is empty"

    try:
        img = Image.open(path)
        img.verify()
    except Exception:
        return None, "Not a valid image file"

    img = Image.open(path)
    img = ImageOps.exif_transpose(img)

    if img.mode != "RGB":
        img = img.convert("RGB")

    if img.width < MIN_SIZE or img.height < MIN_SIZE:
        return None, f"Image too small ({img.width}x{img.height}). Need at least {MIN_SIZE}px."

    if img.width > MAX_SIZE or img.height > MAX_SIZE:
        img.thumbnail((MAX_SIZE, MAX_SIZE))

    return img, None