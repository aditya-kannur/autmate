
from PIL import ImageGrab
import os
import time
from datetime import datetime

# Configuration
IMAGE_FOLDER = "../images_to_scan"
SCAN_DELAY = 10 

# Ensure the image folder exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def take_screenshot_and_save():
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(IMAGE_FOLDER, filename)
    screenshot.save(filepath)
    print(f"[{timestamp}] Saved screenshot: {filename}")
    return filename, filepath

def run_periodic_screenshots():
    print(f"Taking screenshots every {SCAN_DELAY} seconds.\nPress Ctrl+C to stop.\n")
    try:
        while True:
            take_screenshot_and_save()
            time.sleep(SCAN_DELAY)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    run_periodic_screenshots()
