import subprocess   # Used to run external R scripts
import shutil       # Used to copy files
import os           # Used to check if files exist

def run_ctm_analysis(file_name):
    # Define all file paths used in the process
    cleaned_csv = f"C:/Users/anika/ecliptica/cleaned_{file_name}.csv"  # Input file for CTM
    rdata_output = f"C:/Users/anika/ecliptica/CTMmods/ctm5.Rdata"      # Output RData file from CTM
    ctm_output_csv = "C:/Users/anika/ecliptica/CTM10 - Topics With Keywords and Abstracts.csv"  # Output summary CSV from assess_model.R
    final_output_path = f"C:/Users/anika/ecliptica/{file_name}_ctmResults.csv"  # Where the final file will be saved

    print("CTM files loading...")  # Status message

    # Step 1: Run the CTM training R script (ctm_optimized.R)
    try:
        result = subprocess.run(
            ["Rscript", "CTM_Code/ctm_optimized.R", cleaned_csv, "ctm5"],  # Arguments: Rscript, script path, input CSV, output prefix
            check=True,           # Raise exception if R script fails
            capture_output=True,  # Capture standard output and error for logging
            text=True             # Decode output as text (not bytes)
        )
        # Print standard output and error from the R script
        print("🔧 Rscript STDOUT:\n", result.stdout)
        print("🛑 Rscript STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        # If the CTM R script fails, print errors and return None
        print("❌ Error running CTM script.")
        print("🔧 STDOUT:\n", e.stdout)
        print("🛑 STDERR:\n", e.stderr)
        return None, None

    # Step 2: Check that the expected RData file was created
    if not os.path.exists(rdata_output):
        print("❌ CTM script ran but .Rdata file was not created.")
        return None, None

    print("Assessing model, please wait...")  # Status message for assessment

    # Step 3: Run the R script to assess and summarize the model (assess_model.R)
    try:
        assess = subprocess.run(
            ["Rscript", "CTM_Code/assess_model.R", rdata_output, cleaned_csv],  # Arguments: Rscript, model file, original CSV
            check=True,
            capture_output=True,
            text=True
        )
        # Print standard output and error from the assessment R script
        print("🔧 Assess STDOUT:\n", assess.stdout)
        print("🛑 Assess STDERR:\n", assess.stderr)
    except subprocess.CalledProcessError as e:
        # If the assessment script fails, print errors and return None
        print("❌ Error running the Assess model script.")
        print("🔧 Assess STDOUT:\n", e.stdout)
        print("🛑 Assess STDERR:\n", e.stderr)
        return None, None

    # Step 4: Make sure the final output CSV was generated
    if not os.path.exists(ctm_output_csv):
        print(f"❌ Output file {ctm_output_csv} was not generated.")
        return None, None

    # Step 5: Copy the output summary CSV to a new location with a clearer name
    try:
        shutil.copy(ctm_output_csv, final_output_path)
        print(f"✅ Duplicate saved to {final_output_path}")
    except Exception as e:
        print(f"❌ Error copying output file: {e}")
        return None, None

    # Return paths of the final output files
    return final_output_path, rdata_output
