import pyperclip
import pandas as pd
import time
import os
import subprocess
import re
from datetime import datetime
from io import StringIO

def open_publish_or_perish():
    path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Publish or Perish 8.lnk"
    subprocess.Popen(['cmd', '/c', 'start', '', path])
    print("🚀 Opened Publish or Perish")

def close_publish_or_perish():
    subprocess.call(['taskkill', '/F', '/IM', 'Publish or Perish.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("❌ Closed Publish or Perish")

def wait_for_excel_clipboard_and_process():
    open_publish_or_perish()
    print("📋 Waiting for Excel data from clipboard... Please use 'Copy results with Excel header'")

    pyperclip.copy("")
    old_clipboard = ""

    timeout = time.time() + 60
    while time.time() < timeout:
        time.sleep(1)
        current_clipboard = pyperclip.paste()

        if current_clipboard != old_clipboard and "\t" in current_clipboard:
            try:
                df = pd.read_csv(StringIO(current_clipboard), sep="\t")

                if 'Abstract' not in df.columns:
                    print("⚠️ 'Abstract' column not found in copied data.")
                    continue

                # Extract keywords from the first row of the 'Search terms' or similar column
                keyword_col = next((col for col in df.columns if 'search term' in col.lower() or 'query' in col.lower()), None)
                if keyword_col:
                    raw_keyword = str(df[keyword_col].iloc[0])
                else:
                    raw_keyword = "project"

                keyword_slug = raw_keyword.lower().strip().replace(" ", "_").replace("-", "_")
                keyword_slug = ''.join(c for c in keyword_slug if c.isalnum() or c == "_")[:50]

                with open("last_keywords.txt", "w") as f:
                    f.write(keyword_slug)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{keyword_slug}_{timestamp}.xlsx"
                df.to_excel(filename, index=False)

                print(f"✅ Saved copied data to {filename}")
                close_publish_or_perish()
                return filename

            except Exception as e:
                print(f"⚠️ Clipboard parse error: {e}")
        else:
            print("⌛ Waiting...")

        old_clipboard = current_clipboard

    print("⏰ Timeout. No valid Excel content found.")
    return None
