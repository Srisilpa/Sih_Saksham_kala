import os
from PIL import Image
from vision.pipeline import process_image

CANVAS = 1000

passed = 0
failed = 0


def check(label, condition):
    """Records one assertion."""
    global passed, failed
    if condition:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        failed += 1


def test_good_image(path, pid):
    print(f"\n[good image] {path}")

    result = process_image(path, pid)

    check("success is True", result["success"] is True)
    check("error is None", result["error"] is None)

    url = result["image_url"]
    check("image_url is set", bool(url))

    if not url:
        return

    check("url uses forward slashes", "\\" not in url)
    check("url ends with .png", url.endswith(".png"))

    disk_path = url.lstrip("/")
    check("file exists on disk", os.path.exists(disk_path))

    if not os.path.exists(disk_path):
        return

    img = Image.open(disk_path)
    check(f"size is {CANVAS}x{CANVAS}", img.size == (CANVAS, CANVAS))
    check("mode is RGB", img.mode == "RGB")

    size_kb = os.path.getsize(disk_path) / 1024
    check("file under 1000 KB", size_kb < 1000)
    print(f"        ({round(size_kb)} KB)")


def test_bad_image(path, why):
    print(f"\n[bad input] {path}  ({why})")

    try:
        result = process_image(path)
    except Exception as e:
        check("did not crash", False)
        print(f"        crashed with: {e}")
        return

    check("did not crash", True)
    check("success is False", result["success"] is False)
    check("image_url is None", result["image_url"] is None)
    check("error message is present", bool(result["error"]))
    print(f"        error: {result['error']}")


print("=" * 50)
print("IMAGE PIPELINE TESTS")
print("=" * 50)

test_good_image("uploads/images/test1.png", "T001")
test_good_image("uploads/images/dress.png", "T002")

test_bad_image("uploads/images/nothere.jpg", "missing file")
test_bad_image("requirements.txt", "not an image")
test_bad_image("uploads/audio/audio.mp4", "audio file")

print("\n" + "=" * 50)
print(f"PASSED: {passed}   FAILED: {failed}")
print("=" * 50)