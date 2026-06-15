import os
import shutil
from utils import read_from_control

def clean_folder_for_calibration_purposes(metrics_folder):
    if metrics_folder:
        metrics_folder = metrics_folder


    # Ensure the folder exists (create if missing)
    os.makedirs(metrics_folder, exist_ok=True)

    # Clean out all contents inside the folder
    for item in os.listdir(metrics_folder):
        item_path = os.path.join(metrics_folder, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"Cleaned folder: {metrics_folder}")

# do argparse
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean metrics folder before calibration.")
    parser.add_argument("--metrics_folder", type=str, default=None, help="Path to the metrics folder to clean. If not provided, it will be read from the control file.")
    
    args = parser.parse_args()
    
    clean_folder_for_calibration_purposes(args.metrics_folder)
