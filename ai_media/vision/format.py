from PIL import Image

CANVAS_SIZE = 1000
MARGIN = 0.08


def format_for_ecommerce(img):
    """
    Crops to the product, scales it, and centres it on a white square.
    Input:  a Pillow image (ideally RGBA with transparency)
    Output: (formatted_image, error_message)
    """
    try:
        if img.mode == "RGBA":
            box = img.getbbox()
            if box:
                img = img.crop(box)

        usable = int(CANVAS_SIZE * (1 - 2 * MARGIN))

        product = img.copy()
        product.thumbnail((usable, usable), Image.LANCZOS)

        canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))

        x = (CANVAS_SIZE - product.width) // 2
        y = (CANVAS_SIZE - product.height) // 2

        if product.mode == "RGBA":
            canvas.paste(product, (x, y), product)
        else:
            canvas.paste(product, (x, y))

        return canvas, None

    except Exception as e:
        return None, f"Formatting failed: {e}"