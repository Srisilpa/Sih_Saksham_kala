import os
from vision.validate import validate_image
from vision.background import remove_background

INPUT = "uploads/images/test1.png"
OUTPUT = "outputs/images/test1_nobg.png"

img, error = validate_image(INPUT)
if error:
    print("Validation failed:", error)
else:
    print("Validated:", img.size, img.mode)
    print("Removing background... (first run downloads ~170MB)")

    result, error = remove_background(img)
    if error:
        print("Failed:", error)
    else:
        print("Done. Mode is now:", result.mode)
        os.makedirs("outputs/images", exist_ok=True)
        result.save(OUTPUT)
        print("Saved to:", OUTPUT)
        result.show()