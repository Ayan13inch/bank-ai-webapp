import pdfplumber, pandas as pd, io
from PIL import Image
import pytesseract

def parse_pdf_bytes(bts):
    with pdfplumber.open(io.BytesIO(bts)) as pdf:
        rows=[]
        for p in pdf.pages:
            tbl = p.extract_table()
            if tbl:
                for r in tbl[1:]:
                    rows.append(r)
    df = pd.DataFrame(rows)
    return df.to_dict(orient='records')

def parse_statement(content, filename):
    if filename.lower().endswith('.pdf'):
        return parse_pdf_bytes(content)
    # add Excel handling with pandas.read_excel
    return []
