from PIL import ImageGrab
import os
from datetime import datetime
import shutil

IMAGE_FOLDER = "../images_to_scan"
RESULT_FILE = "result.txt"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

def take_screenshot_and_save():
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(IMAGE_FOLDER, filename)
    screenshot.save(filepath)
    print(f"[+] Screenshot saved: {filename}")

def clean_image_folder():
    for f in os.listdir(IMAGE_FOLDER):
        os.remove(os.path.join(IMAGE_FOLDER, f))
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)
    print("🧹 Clean start: Image folder and result.txt cleared.")
