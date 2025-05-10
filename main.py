import os
import time
import signal
import threading
from screenshot_ocr import take_screenshot_and_save, clean_image_folder
from scan import scan_top_image
from pathlib import Path

# Config
IMAGE_FOLDER = "../images_to_scan"
RESULT_FILE = "result.txt"
MAX_IMAGES = 5
SCAN_INTERVAL = 11  # seconds

stop_event = threading.Event()

def graceful_exit(signum, frame):
    stop_event.set()
    print("\n🛑 Stopping gracefully...")

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

def maintain_stack():
    files = sorted(Path(IMAGE_FOLDER).glob("*"), key=os.path.getmtime)
    if len(files) > MAX_IMAGES:
        os.remove(files[0])  # Remove oldest

def worker_loop():
    while not stop_event.is_set():
        try:
            scan_top_image()                            # Scan top image
            take_screenshot_and_save()                  # Add new screenshot
            maintain_stack()                            # Keep stack length
            time.sleep(SCAN_INTERVAL)
        except Exception as e:
            print(f"⚠ Error in loop: {e}")

if __name__ == "__main__":
    clean_image_folder()                                # Clear folder + result.txt
    print(f"🟢 Starting OCR with 10s interval. Press Ctrl+C to stop.\n")
    worker_loop()
    print("✅ Exited cleanly.")
