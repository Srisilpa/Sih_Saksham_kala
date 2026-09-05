import sys
import os
from PIL import Image
import rembg
import openai
from dotenv import load_dotenv

print("Python version:", sys.version.split()[0])
print("Pillow: OK")
print("rembg: OK")
print("openai: OK")

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    print("API key found, starts with:", key[:6])
else:
    print("No API key found in .env")

print("\nPhase 1 setup complete.")