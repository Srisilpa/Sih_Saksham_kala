import os
from vision.validate import validate_image
from vision.background import remove_background
from vision.enhance import enhance_image

INPUT = "uploads/images/test1.png"
BEFORE = "outputs/images/test1_nobg.png"
AFTER = "outputs/images/test1_enhanced.png"

os.makedirs("outputs/images", exist_ok=True)

img, error = validate_image(INPUT)
if error:
    print("Validation failed:", error)
    raise SystemExit

result, error = remove_background(img)
if error:
    print("Background removal failed:", error)
    raise SystemExit

result.save(BEFORE)
print("Saved BEFORE:", BEFORE)

enhanced, error = enhance_image(result)
if error:
    print("Enhancement failed:", error)
    raise SystemExit

enhanced.save(AFTER)
print("Saved AFTER: ", AFTER)
print("Mode:", enhanced.mode, "Size:", enhanced.size)