import os
from vision.validate import validate_image
from vision.background import remove_background
from vision.enhance import enhance_image
from vision.format import format_for_ecommerce

INPUT = "uploads/images/test1.png"
OUTPUT = "outputs/images/test1_final.png"

os.makedirs("outputs/images", exist_ok=True)

img, error = validate_image(INPUT)
if error:
    print("Validation failed:", error)
    raise SystemExit
print("Validated:", img.size)

nobg, error = remove_background(img)
if error:
    print("Background removal failed:", error)
    raise SystemExit
print("Background removed:", nobg.size, nobg.mode)

enhanced, error = enhance_image(nobg)
if error:
    print("Enhancement failed:", error)
    raise SystemExit
print("Enhanced:", enhanced.size)

final, error = format_for_ecommerce(enhanced)
if error:
    print("Formatting failed:", error)
    raise SystemExit

final.save(OUTPUT, "PNG", optimize=True)
print("Final:", final.size, final.mode)
print("Saved:", OUTPUT)
print("File size:", round(os.path.getsize(OUTPUT) / 1024), "KB")