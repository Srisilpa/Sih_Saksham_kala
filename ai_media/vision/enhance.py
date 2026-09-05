from PIL import ImageEnhance

BRIGHTNESS = 1.15
CONTRAST = 1.20
SHARPNESS = 1.30


def enhance_image(img):
    """
    Improves brightness, contrast and sharpness.
    Preserves transparency if present.
    Input:  a Pillow image
    Output: (enhanced_image, error_message)
    """
    try:
        has_alpha = img.mode == "RGBA"

        if has_alpha:
            alpha = img.getchannel("A")
            work = img.convert("RGB")
        else:
            work = img

        work = ImageEnhance.Brightness(work).enhance(BRIGHTNESS)
        work = ImageEnhance.Contrast(work).enhance(CONTRAST)
        work = ImageEnhance.Sharpness(work).enhance(SHARPNESS)

        if has_alpha:
            work = work.convert("RGBA")
            work.putalpha(alpha)

        return work, None

    except Exception as e:
        return None, f"Enhancement failed: {e}"