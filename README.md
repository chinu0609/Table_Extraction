# PDF Table Extractor

This project extracts tables from PDF documents using **pdfplumber** for digital PDFs and **img2table** with **Tesseract OCR** for scanned PDFs. The extracted tables are converted into Pandas DataFrames for further analysis.

## Features

- Extract tables from **digital PDFs** using `pdfplumber`.
- Extract tables from **scanned PDFs** using `img2table` and `Tesseract OCR`.
- Convert extracted tables into Pandas DataFrames.
- Save scanned table data into an Excel file (`tables.xlsx`).
- Streamlit UI available for easy interaction (if applicable).

---

## Installation

### **Step 1: Install Dependencies**

Make sure you have Python 3.8+ installed.

```sh
pip install pdfplumber pandas numpy img2table openpyxl streamlit
```

### **Step 2: Install Tesseract OCR**

Since `img2table` relies on Tesseract for OCR, install it based on your OS:

#### **Windows**

1. Download Tesseract from [Tesseract official repo](https://github.com/UB-Mannheim/tesseract/wiki).
2. Install and add the path to `tesseract.exe` in **System Environment Variables** (e.g., `C:\Program Files\Tesseract-OCR`)
3. Verify installation:
    
    ```sh
    tesseract --version
    ```
    

#### **Linux (Ubuntu/Debian)**

```sh
sudo apt update
sudo apt install tesseract-ocr -y
```

#### **MacOS**

```sh
brew install tesseract
```

---

## Usage

### **Extract Tables from Digital PDFs**

```python
from pdfplumber import open as pdfp_open

tables = get_tables(pdfp_open("./your_document.pdf"))
```

### **Extract Tables from Scanned PDFs (with OCR)**

```python
from img2table.document import PDF

tables = get_tables_scanned(PDF("./your_scanned_document.pdf"))
```

The extracted tables are returned as a **list of Pandas DataFrames**.

---

## Streamlit UI

if you just want to test the project you can run the following.
```sh
streamlit run app.py
```

This will launch a web-based interface where users can upload PDFs and view extracted tables. The UI consists of two options `Scanned` and `Only Text` Scanned is for Scanned pdfs and only text is for normal pdfs. 

---

## Troubleshooting

- **If OCR is not working:** Ensure `Tesseract` is installed and added to the system PATH.
- **If tables are not extracted properly:** Check if the PDF is **scanned** or **digital** and use the appropriate function (`get_tables` or `get_tables_scanned`).
- **Duplicate column errors:** This script renames duplicate columns automatically to avoid conflicts.

---


