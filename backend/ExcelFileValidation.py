import os
import mimetypes
import openpyxl
import pandas as pd

file_path = "Copy of Technology Assessment XLData 2.xlsx"

# Check extension
print(f"File Extension: {os.path.splitext(file_path)[1]}")

# Check MIME type
mime_type, _ = mimetypes.guess_type(file_path)
print(f"MIME Type (guess): {mime_type}")

# Try openpyxl
try:
    wb = openpyxl.load_workbook(file_path, data_only=True)
    print("✅ openpyxl succeeded")
    for sheet in wb.worksheets:
        print(f"Sheet: {sheet.title}")
except Exception as e:
    print(f"❌ openpyxl failed: {e}")

# Try pandas
try:
    df = pd.read_excel(file_path, engine="openpyxl")
    print("✅ pandas succeeded")
    print(df.head())
except Exception as e:
    print(f"❌ pandas failed: {e}")
