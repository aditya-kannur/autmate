# OCR Image Scanner

## 🛠️ Setup Instructions

Follow the steps below to set up and run the OCR Image Scanner:

---

### 1. Create and Activate Virtual Environment

First, create a virtual environment to isolate dependencies.

```bash
# Create a virtual environment
python -m venv venv
```

Activate the virtual environment:

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **On Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Paths

Update the following paths in your code to match your local setup:

```python
# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'path to your downloaded tesseract file'

# Folder containing the images to process
IMAGE_FOLDER = "Folder of your images"

# Output JSON file to store the extracted text
OUTPUT_JSON = "File name to store the text"
```

- **Tesseract Path**: Replace `'path to your downloaded tesseract file'` with the full path to the Tesseract executable on your system.
- **Image Folder**: Specify the folder containing the images you want to scan.
- **Output JSON**: Provide a name for the JSON file where the extracted text will be saved.

---

### 4. Run the OCR Scanner

Once everything is set up, you can run the OCR scanner script:

```bash
python your_script_name.py
```

Replace `your_script_name.py` with the name of your Python script.

---

## 📂 Project Structure

```
Automate/
├── venv/                # Virtual environment folder
├── requirements.txt     # Dependencies file
├── your_script_name.py  # Main script for OCR scanning
├── images/              # Folder containing input images
└── output.json          # Output file with extracted text
```

---

## 📝 Notes

- Ensure that Tesseract OCR is installed on your system. You can download it from [Tesseract's official website](https://github.com/tesseract-ocr/tesseract).
- Use high-quality images for better OCR accuracy.
- If you encounter issues, verify that the paths are correctly configured.

---
