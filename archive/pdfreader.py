import pdfplumber
import pandas as pd

all_tables = []

with pdfplumber.open("scaling_data.pdf") as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv("combined_tables.csv", index=False)
