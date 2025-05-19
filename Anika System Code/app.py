import sys
import os
import zipfile
import subprocess
import shutil
import traceback
import pandas as pd
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from tqdm import tqdm

from PoP_Interface.fetch_from_pop import wait_for_excel_clipboard_and_process
from CTM_Code.clean_abstracts import remove_empty_abstracts
from CTM_Code.ctm_runner import run_ctm_analysis
from CTM_Code.summarize_keywords import generate_summary_topics
from assign_topic_to_row.assign_tor import assign_topics_to_metadata

from Visualization_Code.bar_graph import bar_chart_overview
from Visualization_Code.linechart import line_chart_overview
from Visualization_Code.pie_chart import generate_pie_chart
from Visualization_Code.sum_sunburst import create_sunburst_chart
from Visualization_Code.keyword_network import generate_keyword_network
from Visualization_Code.generate_geo_topic_map import generate_geo_topic_map

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
        root_dir = os.getcwd()
        outputs_dir = os.path.join(root_dir, "outputs")
        os.makedirs(outputs_dir, exist_ok=True)

        # Step 1: Clipboard Input
        print("📋 Starting clipboard extraction...")
        filename = wait_for_excel_clipboard_and_process()
        if not filename or not os.path.exists(filename):
            raise FileNotFoundError("Failed to get valid Excel file from clipboard")

        base_filename = os.path.splitext(os.path.basename(filename))[0]

        # ➕ Use keyword from saved file if available
        try:
            with open("last_keywords.txt", "r") as f:
                keyword_base = f.read().strip()
        except:
            keyword_base = base_filename.lower().replace(" ", "_").replace("-", "_")

        output_folder = os.path.join(outputs_dir, f"{keyword_base}_data")
        zip_path = f"{output_folder}.zip"

        print(f"✅ Clipboard data saved to {filename}")
        steps.update(1)

        # Step 2: Clean Abstracts
        cleaned_csv_path = os.path.join(outputs_dir, f"cleaned_{base_filename}.csv")
        remove_empty_abstracts(filename, cleaned_csv_path)
        if not os.path.exists(cleaned_csv_path):
            raise FileNotFoundError(f"Failed to create cleaned CSV at {cleaned_csv_path}")
        print(f"🧼 Abstracts cleaned and saved to {cleaned_csv_path}")
        steps.update(1)

        # Step 3: Run CTM
        print("⚙️ Running CTM analysis...")
        ctm_output_csv, ctm_rdata_path = run_ctm_analysis(base_filename, cleaned_csv_path)
        print("🔍 CTM analysis complete.")
        steps.update(1)

        # Step 4: Generate Keywords
        if os.path.exists(ctm_output_csv):
            try:
                generate_summary_topics(ctm_output_csv, ctm_output_csv)
                print("🧠 Summary topics generated")
            except Exception as e:
                print(f"⚠️ Failed to generate summary topics: {str(e)}")
        steps.update(1)

        # Step 5: Assign Topics
        assigned_output_path = os.path.join(outputs_dir, f"{base_filename}_with_assigned_topics.xlsx")
        if os.path.exists(cleaned_csv_path) and os.path.exists(ctm_output_csv):
            assign_topics_to_metadata(cleaned_csv_path, ctm_output_csv, assigned_output_path)
            print("🏷️ Topics assigned")
        steps.update(1)

        # Step 6: Organize folders
        cleaned_folder = os.path.join(output_folder, "Cleaned Dataset")
        ctm_folder = os.path.join(output_folder, "CTM Results")
        viz_folder = os.path.join(output_folder, "Visualizations")

        os.makedirs(cleaned_folder, exist_ok=True)
        os.makedirs(ctm_folder, exist_ok=True)
        os.makedirs(viz_folder, exist_ok=True)

        # Step 7: Visualizations
        bar_chart_overview(assigned_output_path, output_folder)
        generate_pie_chart(ctm_output_csv, output_folder)
        create_sunburst_chart(ctm_output_csv, output_folder)
        line_chart_overview(assigned_output_path, output_folder)
        generate_geo_topic_map(ctm_output_csv, output_folder)
        generate_keyword_network(ctm_output_csv, output_folder)
        print("📊 Visualizations done")
        steps.update(1)

        # Step 8: Move files
        files_to_move = [
            (cleaned_csv_path, os.path.join(cleaned_folder, os.path.basename(cleaned_csv_path))),
            (assigned_output_path, os.path.join(cleaned_folder, os.path.basename(assigned_output_path))),
            (ctm_output_csv, os.path.join(ctm_folder, os.path.basename(ctm_output_csv))),
            (ctm_rdata_path, os.path.join(ctm_folder, os.path.basename(ctm_rdata_path)))
        ]

        for src, dst in files_to_move:
            if os.path.exists(src):
                shutil.move(src, dst)

        for extra_file in [
            "CTM10 - Topics With Keywords and Abstracts.csv",
            "CTM10 - Topic Word Matrix.csv",
            "CTM10 - Doc Topic Matrix.csv"
        ]:
            full_path = os.path.join(outputs_dir, extra_file)
            if os.path.exists(full_path):
                shutil.move(full_path, os.path.join(ctm_folder, extra_file))

        print(f"📂 All results saved to: {output_folder}")
        steps.update(1)

        # Step 9: Zip it up
        shutil.make_archive(output_folder, 'zip', output_folder)

        # ✅ Also copy to public outputs
        public_outputs_dir = os.path.join(root_dir, "frontend", "public", "outputs")
        os.makedirs(public_outputs_dir, exist_ok=True)
        shutil.copy(zip_path, os.path.join(public_outputs_dir, os.path.basename(zip_path)))
        print(f"📁 Zip copied to frontend/public/outputs/{os.path.basename(zip_path)}")

        steps.close()

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=os.path.basename(zip_path)
        )

    except Exception as e:
        print("❌ Error during CTM pipeline execution:")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
