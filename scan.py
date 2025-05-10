import pytesseract
from PIL import Image
import os
import cv2
import numpy as np
from fuzzywuzzy import fuzz
from pathlib import Path

# Config
IMAGE_FOLDER = "../images_to_scan"
RESULT_FILE = "text.txt"
TARGET_WORDS = ["monkey", "panda", "pigeion", "rabbit", "swallow", "eagle", "lion", "peacock", "shark"]
FUZZY_MATCH_THRESHOLD = 60
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

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

def scan_top_image():
    files = sorted(Path(IMAGE_FOLDER).glob("*"), key=os.path.getmtime, reverse=True)
    if not files:
        print("⚠ No images to scan.")
        return

    top_image = files[0]
    try:
        img = Image.open(top_image)
        cropped = crop_center_30_percent(img)

        # ✅ Save the cropped image for debugging
        cropped.save("last_cropped_raw.png")

        processed_img = preprocess_image(cropped)

        # ✅ Save the processed image too (after thresholding etc.)
        processed_img.save("last_cropped_processed.png")

        text = pytesseract.image_to_string(
            processed_img, lang='eng', config='--psm 6 --oem 3'
        ).strip()

        print("OCR Text:", text)

        keywords_found = fuzzy_match_keywords(text)
        with open(RESULT_FILE, 'a', encoding='utf-8') as f:
            f.write(', '.join(keywords_found) if keywords_found else "None")
            f.write('\n')

        print(f"[SCAN] {top_image.name}: {keywords_found or 'None'}")

    except Exception as e:
        print(f"⚠ Error scanning {top_image.name}: {e}")
