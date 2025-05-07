import pytesseract
from PIL import Image
import os
import json
import cv2
import numpy as np
from datetime import datetime
from fuzzywuzzy import fuzz

# Configuration
IMAGE_FOLDER = "../images_to_scan"
OUTPUT_JSON = "results.json"
TARGET_WORDS = ["monkey", "panda", "peigion", "rabbit"]
FUZZY_MATCH_THRESHOLD = 60 
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return Image.fromarray(processed)

def crop_center_30_percent(image):
    width, height = image.size
    w_crop = int(width * 0.3)
    h_crop = int(height * 0.3)
    left = (width - w_crop) // 2
    top = (height - h_crop) // 2
    right = left + w_crop
    bottom = top + h_crop
    return image.crop((left, top, right, bottom))

def fuzzy_match_keywords(text):
    matches = []
    for word in text.split():
        for keyword in TARGET_WORDS:
            if fuzz.ratio(word.lower(), keyword.lower()) >= FUZZY_MATCH_THRESHOLD:
                matches.append(keyword)
    return list(set(matches)) 

def scan_images():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder '{IMAGE_FOLDER}' not found")
        return

    print(f"Scanning images in: {os.path.abspath(IMAGE_FOLDER)}\n")
    results = []

    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            filepath = os.path.join(IMAGE_FOLDER, filename)

            try:
                img = Image.open(filepath)
                cropped = crop_center_30_percent(img)
                processed_img = preprocess_image(cropped)

                text = pytesseract.image_to_string(
                    processed_img,
                    lang='eng',
                    config='--psm 6 --oem 3'
                ).strip()

                keywords_found = fuzzy_match_keywords(text)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                result_entry = {
                    "filename": filename,
                    "timestamp": timestamp,
                    "found_keywords": keywords_found,
                    "text": text
                }

                results.append(result_entry)

                with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)

                print(f"[{timestamp}] Processed: {filename}")
                print(f"   Found: {keywords_found or 'None'}")
                print("-" * 50)

            except Exception as e:
                print(f"⚠ Error processing {filename}: {str(e)}")

    print(f"\nScan complete. Results saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    scan_images()
