from vision.validate import validate_image

files = [
    "uploads/images/test1.png",
    "uploads/images/test2.jpg",
    "uploads/images/nothere.jpg",
    "requirements.txt",
]

for f in files:
    img, error = validate_image(f)
    if error:
        print(f"FAIL  {f}  ->  {error}")
    else:
        print(f"OK    {f}  ->  {img.size}  mode={img.mode}")