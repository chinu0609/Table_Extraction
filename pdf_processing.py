import pdfplumber as pdfp
import pandas as pd
import numpy as np
from img2table.document import PDF
from img2table.ocr import TesseractOCR


def get_tables(file):
    tables = [] 
    for page in file.pages:  
        all_data = page.extract_tables()
        if len(all_data) != 0 :

            all_data = np.array(all_data)
         
            x,y,z = all_data.shape
            all_data = all_data.reshape(y,z) 

            values = all_data[1:]
            columns = all_data[0]

            df = pd.DataFrame(values)
            df.columns = pd.Series(df.columns).astype(str)  # Convert to string (to avoid integer column issues)
            df.columns = [f"{col}_{i}" if df.columns.duplicated()[i] else col for i, col in enumerate(df.columns)]
            tables.append(df)
    return tables

def get_tables_scanned(file):
    
    ocr = TesseractOCR(lang="eng")

    pdf_tables = file.extract_tables(ocr=ocr)
    
    file.to_xlsx('tables.xlsx',
                ocr=ocr)
    return list(pd.read_excel('tables.xlsx',sheet_name=None).values())
     




if __name__ == "__main__":
    tables = get_tables_scanned(PDF('./stock_market_dataset.pdf'))
    

