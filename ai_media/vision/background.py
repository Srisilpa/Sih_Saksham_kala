from rembg import remove, new_session

_session = None


def get_session():
    """Creates the AI model session once and reuses it."""
    global _session
    if _session is None:
        _session = new_session("u2net")
    return _session


def remove_background(img):
    """
    Removes the background from a product image.
    Input:  a Pillow image (from validate_image)
    Output: (image_with_transparency, error_message)
    """
    try:
        session = get_session()
        result = remove(img, session=session)
        return result, None
    except Exception as e:
        return None, f"Background removal failed: {e}"