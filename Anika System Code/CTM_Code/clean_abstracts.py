import pandas as pd
import os

def remove_empty_abstracts(input_excel_path, output_csv_path):
    """
    Loads the Excel metadata file, removes rows with missing or empty abstracts,
    and writes the cleaned data to a CSV file.
    """
    # Check that input file exists
    if not os.path.exists(input_excel_path):
        raise FileNotFoundError(f"❌ Input file not found: {input_excel_path}")

    # Read Excel
    df = pd.read_excel(input_excel_path)
    print(f"📄 Loaded {len(df)} rows from {input_excel_path}")

    # Ensure 'Abstract' column exists
    if 'Abstract' not in df.columns:
        raise ValueError("❌ 'Abstract' column not found in the input Excel file.")

    # 🧹 Filter out rows with empty or NaN abstracts
    df_cleaned = df[df['Abstract'].notna() & df['Abstract'].str.strip().astype(bool)]
    print(f"🧼 Retained {len(df_cleaned)} rows after removing empty abstracts.")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Save cleaned CSV
    df_cleaned.to_csv(output_csv_path, index=False)
    print(f"✅ Cleaned data saved to {output_csv_path}")

    return output_csv_path
