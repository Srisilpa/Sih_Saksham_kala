from vision.pipeline import process_image

cases = [
    ("uploads/images/test1.png", "P001"),
    ("uploads/images/image.jpg", "P002"),
    ("uploads/images/dress.png", "P003"),
    ("requirements.txt", "P004"),
]

for path, pid in cases:
    print("\n---", path, "---")
    result = process_image(path, pid)
    print(result)

print("\n--- auto-generated ID ---")
print(process_image("uploads/images/test1.png"))