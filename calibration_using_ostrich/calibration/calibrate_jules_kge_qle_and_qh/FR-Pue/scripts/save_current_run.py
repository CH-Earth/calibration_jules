#!/usr/bin/env python3
import os
import pandas as pd
from glob import glob
from datetime import datetime
import argparse

def main(base_folder, output_folder):
    # Make sure results directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Current datetime (once for the whole run)
    run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    runs_folder = os.path.join(base_folder, "ost")
    if not os.path.isdir(runs_folder):
        print(f"⚠️ Skipping {base_folder}: folder not found.")
        

    files = glob(os.path.join(runs_folder, "OstModel*.txt"))
    if not files:
        print(f"⚠️ No OstModel*.txt files for {base_folder}.")
        

    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, delim_whitespace=True, engine="python")
            #df["source_file"] = os.path.basename(f)   # filename
            df["source_file"] = os.path.realpath(f)   # full resolved path
            df["run_datetime"] = run_datetime         # timestamp for run
            dfs.append(df)
        except Exception as e:
            print(f"❌ Error reading {f}: {e}")

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        out_path = os.path.join(output_folder, f"summary.txt")

        if os.path.exists(out_path):
            # Append without header
            combined.to_csv(out_path, sep=",", index=False, mode="a", header=False)
            print(f"➕ Appended to {out_path}")
        else:
            # Write with header
            combined.to_csv(out_path, sep=",", index=False)
            print(f"✅ Created {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate OstModel*.txt files for multiple runs."
    )
    parser.add_argument(
        "--base_folder", required=True,
        help="Base input folder containing run subdirectories."
    )
    parser.add_argument(
        "--output_folder", required=True,
        help="Folder where results will be written."
    )
    args = parser.parse_args()
    main(args.base_folder, args.output_folder)
