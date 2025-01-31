import torch
import pandas as pd
import pytesseract
import numpy as np
import cv2
from transformers import TableTransformerForObjectDetection, DetrImageProcessor
from pdf2image import convert_from_path

# Load Table Transformer model
processor = DetrImageProcessor.from_pretrained("microsoft/table-transformer-detection")
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

# Convert PDF to image
pdf_path = "scanned_table.pdf"
pages = convert_from_path(pdf_path, 300)  # Convert PDF to high-quality images

dataframes = []  # Store extracted tables as DataFrames

for page_num, page in enumerate(pages):
    image_np = np.array(page)

    # Convert image to tensor
    inputs = processor(images=image_np, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract table bounding boxes
    target_sizes = torch.tensor([image_np.shape[:2]])  # Image height, width
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        if score > 0.7:  # Confidence threshold
            x, y, w, h = box.int().tolist()
            table_roi = image_np[y:y+h, x:x+w]  # Crop detected table

            # Convert table image to text using Tesseract OCR
            extracted_text = pytesseract.image_to_string(table_roi, config="--psm 6")

            # Convert to structured DataFrame
            table_data = [line.split() for line in extracted_text.split("\n") if line.strip()]
            df = pd.DataFrame(table_data)
            dataframes.append(df)

            print(f"Extracted Table {len(dataframes)}:")
            print(df)

# Save all tables as CSV or Excel
if dataframes:
    with pd.ExcelWriter("extracted_tables.xlsx") as writer:
        for i, df in enumerate(dataframes):
            df.to_excel(writer, sheet_name=f"Table_{i+1}")

print("Tables saved to extracted_tables.xlsx")
#Chinmay Hemant Bhosale
