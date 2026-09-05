from audio.language import check_language

cases = [
    ("en", 0.98),
    ("hi", 0.99),
    ("te", 0.95),
    ("hi", 0.55),
    ("mr", 0.60),
]

for code, conf in cases:
    result = check_language(code, conf)
    print(f"{code} @ {conf}")
    print(f"   -> {result}")
    print()