import subprocess
import shutil
import os
import sys
import glob

HARDCODED_RSCRIPT = r"C:\Program Files\R\R-4.5.0\bin\Rscript.exe"

def find_rscript():
    if shutil.which("Rscript"):
        return "Rscript"
    if os.path.exists(HARDCODED_RSCRIPT):
        return HARDCODED_RSCRIPT
    raise FileNotFoundError("❌ Rscript executable not found.")

def run_ctm_analysis(base_filename, cleaned_csv):
    rscript = find_rscript()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_base = os.path.join(base_dir, "outputs")
    os.makedirs(output_base, exist_ok=True)
    os.makedirs(os.path.join(output_base, "CTMmods"), exist_ok=True)

    rdata_output = os.path.join(output_base, "CTMmods", "ctm5.Rdata")
    ctm_output_csv = os.path.join(output_base, "CTMmods", "CTM10 - Topics With Keywords and Abstracts.csv")
    final_output_path = os.path.join(output_base, f"{base_filename}_ctmResults.csv")

    print("📦 CTM files loading...")

    try:
        result = subprocess.run(
            [rscript, os.path.join("CTM_Code", "ctm_optimized.R"), cleaned_csv, "ctm5", output_base],
            check=True,
            capture_output=True,
            text=True
        )
        # Print standard output and error from the R script
        print("🔧 Rscript STDOUT:\n", result.stdout)
        print("🛑 Rscript STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Error running CTM script.\n🔧 STDOUT:\n{e.stdout}\n🛑 STDERR:\n{e.stderr}")

    # Step 2: Check that the expected RData file was created
    if not os.path.exists(rdata_output):
        raise FileNotFoundError(f"❌ CTM .Rdata file not found at {rdata_output}")

    # Step 3: Run the R script to assess and summarize the model (assess_model.R)
    try:
        assess = subprocess.run(
            [rscript, os.path.join("CTM_Code", "assess_model.R"), rdata_output, cleaned_csv],
            check=True,
            capture_output=True,
            text=True
        )
        # Print standard output and error from the assessment R script
        print("🔧 Assess STDOUT:\n", assess.stdout)
        print("🛑 Assess STDERR:\n", assess.stderr)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Error running the Assess model script.\n🔧 STDOUT:\n{e.stdout}\n🛑 STDERR:\n{e.stderr}")

    # Step 4: Make sure the final output CSV was generated
    if not os.path.exists(ctm_output_csv):
        raise FileNotFoundError(f"❌ CTM output CSV not found at {ctm_output_csv}")

    # Step 5: Copy the output summary CSV to a new location with a clearer name
    try:
        shutil.copy(ctm_output_csv, final_output_path)
        print(f"✅ Duplicate saved to {final_output_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Error copying output file: {str(e)}")

    # Return paths of the final output files
    return final_output_path, rdata_output




# import subprocess
# import shutil
# import os

# def run_ctm_analysis(file_name):
#     cleaned_csv = f"C:/Users/anika/ecliptica/cleaned_{file_name}.csv"
#     rdata_output = f"C:/Users/anika/ecliptica/CTMmods/ctm5.Rdata"
#     ctm_output_csv = "C:/Users/anika/ecliptica/CTM10 - Topics With Keywords and Abstracts.csv"
#     final_output_path = f"C:/Users/anika/ecliptica/{file_name}_ctmResults.csv"

#     print("CTM files loading...")

#     try:
#         result = subprocess.run(
#             ["Rscript", "CTM_Code/ctm_optimized.R", cleaned_csv, "ctm5"],
#             check=True,
#             capture_output=True,
#             text=True
#         )
#         print("🔧 Rscript STDOUT:\n", result.stdout)
#         print("🛑 Rscript STDERR:\n", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print("❌ Error running CTM script.")
#         print("🔧 STDOUT:\n", e.stdout)
#         print("🛑 STDERR:\n", e.stderr)
#         return None, None

#     if not os.path.exists(rdata_output):
#         print("❌ CTM script ran but .Rdata file was not created.")
#         return None, None

#     print("Assessing model, please wait...")

#     try:
#         assess = subprocess.run(
#             ["Rscript", "CTM_Code/assess_model.R", rdata_output, cleaned_csv],
#             check=True,
#             capture_output=True,
#             text=True
#         )
#         print("🔧 Assess STDOUT:\n", assess.stdout)
#         print("🛑 Assess STDERR:\n", assess.stderr)
#     except subprocess.CalledProcessError as e:
#         print("❌ Error running the Assess model script.")
#         print("🔧 Assess STDOUT:\n", e.stdout)
#         print("🛑 Assess STDERR:\n", e.stderr)
#         return None, None

#     if not os.path.exists(ctm_output_csv):
#         print(f"❌ Output file {ctm_output_csv} was not generated.")
#         return None, None

#     try:
#         shutil.copy(ctm_output_csv, final_output_path)
#         print(f"✅ Duplicate saved to {final_output_path}")
#     except Exception as e:
#         print(f"❌ Error copying output file: {e}")
#         return None, None

#     return final_output_path, rdata_output
