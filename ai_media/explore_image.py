from PIL import Image, ImageOps

path = "uploads/images/image.png"

img = Image.open(path)

print("--- BEFORE rotation fix ---")
print("Format :", img.format)
print("Mode   :", img.mode)
print("Size   :", img.size)
print("Width  :", img.width)
print("Height :", img.height)

img = ImageOps.exif_transpose(img)

print("\n--- AFTER rotation fix ---")
print("Size   :", img.size)

megapixels = (img.width * img.height) / 1_000_000
print("Megapixels:", round(megapixels, 1))

if img.width > img.height:
    print("Shape  : landscape (wide)")
elif img.height > img.width:
    print("Shape  : portrait (tall)")
else:
    print("Shape  : square")

img.show()