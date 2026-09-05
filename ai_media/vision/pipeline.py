import os
import uuid

from vision.validate import validate_image
from vision.background import remove_background
from vision.enhance import enhance_image
from vision.format import format_for_ecommerce

OUTPUT_DIR = "outputs/images"


def _fail(message):
    """Builds a failure response."""
    return {
        "success": False,
        "image_url": None,
        "error": message
    }


def process_image(input_path, product_id=None):
    """
    Full image pipeline for artisan product photos.

    Input:
        input_path  - path to the uploaded photo
        product_id  - optional ID used for the output filename

    Output: dict with success, image_url, error
    """

    if product_id is None:
        product_id = uuid.uuid4().hex[:8]

    img, error = validate_image(input_path)
    if error:
        return _fail(error)

    img, error = remove_background(img)
    if error:
        return _fail(error)

    img, error = enhance_image(img)
    if error:
        return _fail(error)

    img, error = format_for_ecommerce(img)
    if error:
        return _fail(error)

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{product_id}.png")
        img.save(output_path, "PNG", optimize=True)
    except Exception as e:
        return _fail(f"Could not save image: {e}")

    return {
        "success": True,
        "image_url": "/" + output_path.replace("\\", "/"),
        "error": None
    }