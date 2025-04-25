import pytesseract
from PIL import Image
import os
import json
import cv2
import numpy as np
import time
from datetime import datetime

# Configuration
IMAGE_FOLDER = "../images_to_scan"  
OUTPUT_JSON = "results.json"    
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
SCAN_DELAY = 10  

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return Image.fromarray(processed)


def scan_images():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder '{IMAGE_FOLDER}' not found")
        return

    print(f" Rescanning ALL images in: {os.path.abspath(IMAGE_FOLDER)}")
    print(f" Delay between scans: {SCAN_DELAY} seconds\n")

    results = []  

    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            filepath = os.path.join(IMAGE_FOLDER, filename)
            
            try:
                # OCR Processing
                img = Image.open(filepath)
                processed_img = preprocess_image(img)
                text = pytesseract.image_to_string(
                    processed_img,
                    lang='eng',
                    config='--psm 6 --oem 3'
                ).strip()
                
                # Filter keywords
                filtered_text = text
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                filtered_text = filtered_text.split("\n")

                # Append result
                results.append( filtered_text,)

                # Save incrementally 
                with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)

                print(f" [{timestamp}] Processed: {filename}")
                print(f"   Keywords: {filtered_text or 'None'}")
                print("-" * 50)

            except Exception as e:
                print(f"⚠ Error processing {filename}: {str(e)}")

            # Delay before next scan
            # time.sleep(SCAN_DELAY)

    print(f"\n Rescan complete. Fresh results saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    scan_images()