import pyperclip          # To access the system clipboard
import pandas as pd       # For working with DataFrames and saving Excel files
import time               # For sleep/delay while checking the clipboard
import os                 # For file/path operations (used indirectly here)
import subprocess         # To run other programs like opening/closing Publish or Perish
from datetime import datetime  # For creating unique timestamps in filenames
from io import StringIO   # To read clipboard text as if it were a file

# Function to open the Publish or Perish program
def open_publish_or_perish():
    path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Publish or Perish 8.lnk"  # Shortcut path
    subprocess.Popen(['cmd', '/c', 'start', '', path])  # Open the shortcut using cmd
    print(f"🚀 Opened Publish or Perish")

# Function to forcefully close Publish or Perish
def close_publish_or_perish():
    subprocess.call(
        ['taskkill', '/F', '/IM', 'Publish or Perish.exe'],  # Force kill the process
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL  # Hide console output
    )
    print("❌ Closed Publish or Perish")

# Main function to wait for Excel-format data copied from Publish or Perish
def wait_for_excel_clipboard_and_process():
    open_publish_or_perish()  # Step 1: Open the program
    print("📋 Waiting for Excel data from clipboard... Please use 'Copy as Excel with Header'")

    pyperclip.copy("")  # Step 2: Clear clipboard at the start so we don't process old data
    old_clipboard = ""  # Used to compare new vs old clipboard content

    while True:
        time.sleep(1)  # Step 3: Wait 1 second before checking clipboard again
        current_clipboard = pyperclip.paste()  # Get current clipboard content

        # Step 4: If clipboard has changed and contains tabs (means it's Excel-like table)
        if current_clipboard != old_clipboard and "\t" in current_clipboard:
            try:
                # Step 5: Try converting clipboard string to a pandas DataFrame
                df = pd.read_csv(StringIO(current_clipboard), sep="\t")

                # Step 6: Generate a unique filename using current date and time
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"pop_data_{timestamp}.xlsx"

                # Step 7: Save the DataFrame to Excel
                df.to_excel(save_path, index=False)
                print(f"✅ Saved copied data to {save_path}")

                # Step 8: Close Publish or Perish after data is captured
                close_publish_or_perish()

                # Step 9: Return the saved Excel file path
                return save_path
            except Exception as e:
                # Step 10: Handle any unexpected errors in parsing or saving
                print(f"⚠️ Error: {e}")
        else:
            # If clipboard hasn't changed or isn't valid, wait and retry
            print("⌛ Waiting for new clipboard content...")

        # Update old_clipboard so we can detect new content
        old_clipboard = current_clipboard
