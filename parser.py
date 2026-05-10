import io
import pandas as pd

# Optional imports for PDFs and OCR
try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    from pdf2image import convert_from_bytes
    import pytesseract
    from PIL import Image
except Exception:
    convert_from_bytes = None
    pytesseract = None

def parse_pdf_bytes(bts):
    """
    Try structured extraction with pdfplumber first.
    Fallback to OCR if table extraction fails and pdf2image+pytesseract are available.
    Returns list of transaction dicts.
    """
    rows = []
    if pdfplumber:
        with pdfplumber.open(io.BytesIO(bts)) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table and len(table) > 1:
                    headers = table[0]
                    for r in table[1:]:
                        # map header->value
                        rec = {str(headers[i]).strip(): (r[i] if i < len(r) else "") for i in range(len(headers))}
                        rows.append(rec)
    # If no rows found and OCR available, try OCR fallback
    if not rows and convert_from_bytes and pytesseract:
        images = convert_from_bytes(bts, dpi=200)
        for img in images:
            txt = pytesseract.image_to_string(img)
            # very simple line parsing fallback
            for line in txt.splitlines():
                line = line.strip()
                if not line:
                    continue
                # naive heuristic: lines with a date-like token and amount-like token
                if any(ch.isdigit() for ch in line) and ("." in line or "," in line):
                    rows.append({"raw": line})
    return rows

def parse_excel_bytes(bts):
    df = pd.read_excel(io.BytesIO(bts), engine="openpyxl")
    # normalize columns and convert to list of dicts
    df = df.fillna("")
    return df.to_dict(orient="records")

def parse_statement(content, filename="statement"):
    """
    Detect file type by filename and route to appropriate parser.
    Returns list of dicts representing transactions or parsed rows.
    """
    name = filename.lower()
    if name.endswith(".pdf"):
        return parse_pdf_bytes(content)
    if name.endswith(".xls") or name.endswith(".xlsx"):
        return parse_excel_bytes(content)
    # try to guess by magic bytes for Excel
    if content[:4] == b"%PDF":
        return parse_pdf_bytes(content)
    # fallback: try to decode as CSV/TSV
    try:
        s = content.decode("utf-8")
        df = pd.read_csv(io.StringIO(s))
        return df.fillna("").to_dict(orient="records")
    except Exception:
        return [{"raw_bytes_length": len(content), "filename": filename}]
