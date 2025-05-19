import sys
import os
import zipfile
import subprocess
import shutil
import traceback
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from tqdm import tqdm

# Add current and nested folders to the system path
sys.path.append(os.path.abspath("."))

# Local imports
from PoP_Interface.fetch_from_pop import wait_for_excel_clipboard_and_process
from CTM_Code.clean_abstracts import remove_empty_abstracts
from CTM_Code.ctm_runner import run_ctm_analysis
from CTM_Code.summarize_keywords import generate_summary_topics
from assign_topic_to_row.assign_tor import assign_topics_to_metadata

# Visualization imports
from Visualization_Code.generate_geo_topic_map import generate_geo_topic_map
from Visualization_Code.bar_graph import bar_chart_overview
from Visualization_Code.linechart import line_chart_overview
from Visualization_Code.pie_chart import generate_pie_chart
from Visualization_Code.sum_sunburst import create_sunburst_chart
from Visualization_Code.keyword_network import generate_keyword_network


print("✅ Flask app is loaded and waiting...")

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.debug = True

@app.route('/run_ctm', methods=['POST'])
def run_pipeline():
    print("🚨 Received POST /run_ctm request")
    try:
        steps = tqdm(total=8, desc="🔄 Running CTM pipeline", ncols=80)

        # Step 1: Get file from Publish or Perish
        print("📋 Starting clipboard extraction...")
        filename = wait_for_excel_clipboard_and_process()
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        print(f"✅ Clipboard data saved to {filename}")
        steps.update(1)

        # Step 2: Clean abstracts
        input_path = f"{base_filename}.xlsx"
        cleaned_csv_path = f"C:/Users/anika/ecliptica/cleaned_{base_filename}.csv"
        cleaned_xlsx_path = f"C:/Users/anika/ecliptica/cleaned_{base_filename}.xlsx"
        remove_empty_abstracts(input_path, cleaned_csv_path)
        print("🧼 Abstracts cleaned")
        steps.update(1)

        # Step 3: Run CTM
        ctm_output_csv, ctm_rdata_path = run_ctm_analysis(base_filename)
        print("🔍 CTM analysis complete")
        steps.update(1)

        # Step 4: Generate summary topics using YAKE
        generate_summary_topics(ctm_output_csv, ctm_output_csv)
        print("🧠 Summary topics generated using YAKE")
        steps.update(1)

        # Step 5: Assign topics to rows
        assigned_output_path = f"C:/Users/anika/ecliptica/{base_filename}_with_assigned_topics.xlsx"
        assign_topics_to_metadata(cleaned_csv_path, ctm_output_csv, assigned_output_path)
        print("🏷️ Topics assigned to metadata")
        steps.update(1)

        # 🔁 Moved Output Folder Setup BEFORE Visualizations
        output_base = "C:/Users/anika/ecliptica"
        existing = [f for f in os.listdir(output_base) if f.startswith("Outputs")]
        nums = [int(f[7:]) for f in existing if f[7:].isdigit()]
        next_num = max(nums) + 1 if nums else 1
        output_folder = os.path.join(output_base, f"Outputs{next_num}")
        os.makedirs(output_folder, exist_ok=True)

        # Subfolders
        cleaned_folder = os.path.join(output_folder, "Cleaned Dataset")
        ctm_folder = os.path.join(output_folder, "CTM Results")
        viz_folder = os.path.join(output_folder, "Visualizations")

        os.makedirs(cleaned_folder, exist_ok=True)
        os.makedirs(ctm_folder, exist_ok=True)
        os.makedirs(viz_folder, exist_ok=True)

        # Step 6: Run visualizations into correct folder
        bar_chart_overview(assigned_output_path, output_folder)
        generate_pie_chart(ctm_output_csv, output_folder)
        create_sunburst_chart(ctm_output_csv, output_folder)
        line_chart_overview(assigned_output_path, output_folder)
        generate_geo_topic_map(ctm_output_csv, output_folder)
        generate_keyword_network(ctm_output_csv, output_folder)
        

        print("📊 Visualizations generated")
        steps.update(1)

        # Step 7: Move cleaned and CTM result files into subfolders
        shutil.move(cleaned_csv_path, os.path.join(cleaned_folder, os.path.basename(cleaned_csv_path)))
        shutil.move(assigned_output_path, os.path.join(cleaned_folder, os.path.basename(assigned_output_path)))
        shutil.move(ctm_output_csv, os.path.join(ctm_folder, os.path.basename(ctm_output_csv)))
        shutil.move(ctm_rdata_path, os.path.join(ctm_folder, os.path.basename(ctm_rdata_path)))
        shutil.move(f"{output_base}/CTM10 - Topics With Keywords and Abstracts.csv", os.path.join(ctm_folder, "CTM10 - Topics With Keywords and Abstracts.csv"))
        shutil.move(f"{output_base}/CTM10 - Topic Word Matrix.csv", os.path.join(ctm_folder, "CTM10 - Topic Word Matrix.csv"))
        shutil.move(f"{output_base}/CTM10 - Doc Topic Matrix.csv", os.path.join(ctm_folder, "CTM10 - Doc Topic Matrix.csv"))

        print(f"📂 All results saved to: {output_folder}")
        steps.update(1)

        # ✅ Zip the output folder
        shutil.make_archive(output_folder, 'zip', output_folder)

        steps.close()
        from flask import send_file

        zip_path = f"{output_folder}.zip"
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=os.path.basename(zip_path)
)


    except Exception as e:
        print("❌ Error during CTM pipeline execution:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
