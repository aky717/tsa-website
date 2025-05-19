import pandas as pd  # Import the pandas library for data manipulation

def remove_empty_abstracts(input_file, output_file):
    # Read the input Excel file into a DataFrame
    df = pd.read_excel(input_file)  

    # Keep only the rows where the 'Abstract' column is not NaN (not empty/missing)
    df = df[df['Abstract'].notna()]

    # Also remove rows where 'Abstract' is just spaces (e.g., "     ")
    df = df[df['Abstract'].str.strip() != '']

    # Write the cleaned DataFrame to a CSV file (you can change to_excel if needed)
    df.to_csv(output_file, index=False)  # index=False so it doesn't write row numbers

    # Return the output file path for confirmation/logging
    return output_file
