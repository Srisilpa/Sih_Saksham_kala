import os
import time
from audio.pipeline import process_audio

REQUIRED_KEYS = [
    "success", "text", "language", "language_name",
    "supported", "confidence", "warning", "error"
]

MIN_CONFIDENCE = 0.6

passed = 0
failed = 0
transcripts = {}


def check(label, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        failed += 1


def check_contract(result):
    """Every response must have every key, success or failure."""
    missing = [k for k in REQUIRED_KEYS if k not in result]
    check("all contract keys present", not missing)
    if missing:
        print(f"        missing: {missing}")


def test_good_audio(path, expected_lang):
    print(f"\n[good audio] {path}")

    start = time.time()
    try:
        result = process_audio(path)
    except Exception as e:
        check("did not crash", False)
        print(f"        crashed with: {e}")
        return
    elapsed = round(time.time() - start, 1)

    check("did not crash", True)
    check_contract(result)
    check("success is True", result["success"] is True)

    if not result["success"]:
        print(f"        error: {result['error']}")
        return

    check("error is None", result["error"] is None)
    check("text is not empty", bool(result["text"]))
    check("text has real words", len(result["text"].split()) >= 2)
    check(f"language is {expected_lang}", result["language"] == expected_lang)
    check("language is supported", result["supported"] is True)
    check(f"confidence above {MIN_CONFIDENCE}", result["confidence"] > MIN_CONFIDENCE)

    transcripts[path] = result["text"]

    print(f"        {elapsed}s | {result['language_name']} | conf {result['confidence']}")
    if result["warning"]:
        print(f"        warning: {result['warning']}")


def test_bad_audio(path, why):
    print(f"\n[bad input] {path}  ({why})")

    try:
        result = process_audio(path)
    except Exception as e:
        check("did not crash", False)
        print(f"        crashed with: {e}")
        return

    check("did not crash", True)
    check_contract(result)
    check("success is False", result["success"] is False)
    check("text is None", result["text"] is None)
    check("error message is present", bool(result["error"]))
    print(f"        error: {result['error']}")


print("=" * 50)
print("AUDIO PIPELINE TESTS")
print("=" * 50)

test_good_audio("uploads/audio/audio.mp4", "en")
test_good_audio("uploads/audio/hindi.mp4", "hi")

test_bad_audio("uploads/audio/missing.m4a", "missing file")
test_bad_audio("requirements.txt", "not audio")
test_bad_audio("uploads/images/test1.png", "image file")

if transcripts:
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/transcripts.txt", "w", encoding="utf-8") as f:
        for path, text in transcripts.items():
            f.write(f"{path}\n{text}\n\n")
    print("\nTranscripts written to outputs/transcripts.txt")

print("\n" + "=" * 50)
print(f"PASSED: {passed}   FAILED: {failed}")
print("=" * 50)
print("\nNow READ outputs/transcripts.txt and judge accuracy yourself.")