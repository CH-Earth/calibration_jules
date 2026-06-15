import pandas as pd
import HydroErr as he
import numpy as np
import xarray as xr
import os
import glob
import warnings as wg
from datetime import datetime
from pathlib import Path
import argparse
wg.filterwarnings("ignore")

def process_sim(file_xr, flux):
    df = file_xr[flux].to_dataframe().reset_index()
    df.set_index("time", inplace=True)
    return df[flux]


def compute_metrics(folder_with_observations, folder_with_simulations, site, calibration_begining_date, calibration_end_date, validation_begining_date, validation_end_date):
    print(f"Computing metrics for site: {site}")
    
    # Observations
    obs_file = os.path.join(folder_with_observations, f"{site}.nc")
    obs_xr = xr.open_dataset(obs_file)
    obs_df = obs_xr.to_dataframe().reset_index()
    obs_df.set_index("time", inplace=True)

    obs_Qle = obs_df["Qle"]
    obs_Qh = obs_df["Qh"]
    obs_GPP = obs_df["GPP"]
    obs_NEE = obs_df["NEE"]

    # Simulations

    # find using glob a file that says local in folder_with_observations
    sim_files = glob.glob(os.path.join(folder_with_simulations, "*local*"))
    sim_file = sim_files[0]
    sim_xr = xr.open_dataset(sim_file)
    sim_Qle = process_sim(sim_xr, "Qle")
    sim_Qh = process_sim(sim_xr, "Qh")

    combined_Qle = pd.concat([obs_Qle, sim_Qle], axis=1, keys=["obs_Qle", "sim_Qle"])
    combined_Qh = pd.concat([obs_Qh, sim_Qh], axis=1, keys=["obs_Qh", "sim_Qh"])

    calibration_period_Qle = combined_Qle.loc[calibration_begining_date:calibration_end_date, ["obs_Qle", "sim_Qle"]]
    validation_period_Qle = combined_Qle.loc[validation_begining_date:validation_end_date, ["obs_Qle", "sim_Qle"]]
    calibration_period_Qh = combined_Qh.loc[calibration_begining_date:calibration_end_date, ["obs_Qh", "sim_Qh"]]
    validation_period_Qh = combined_Qh.loc[validation_begining_date:validation_end_date, ["obs_Qh", "sim_Qh"]]



    # metrics for calibration period
    kge2012_calibration_Qle = he.kge_2012(calibration_period_Qle["obs_Qle"], calibration_period_Qle["sim_Qle"])
    kge2012_validation_Qle = he.kge_2012(validation_period_Qle["obs_Qle"], validation_period_Qle["sim_Qle"])

    kge2012_calibration_Qh = he.kge_2012(calibration_period_Qh["obs_Qh"], calibration_period_Qh["sim_Qh"])
    kge2012_validation_Qh = he.kge_2012(validation_period_Qh["obs_Qh"], validation_period_Qh["sim_Qh"])

    kge2012_calibration_Qle_and_Qh = np.nanmean([kge2012_calibration_Qle, kge2012_calibration_Qh])
    kge2012_validation_Qle_and_Qh = np.nanmean([kge2012_validation_Qle, kge2012_validation_Qh])


    with open("../flow_stats.txt", "w") as text_file:
        text_file.write("KGE: %f \n" % kge2012_calibration_Qle_and_Qh) # L 0
        text_file.write("LOG NSE: %f \n" % kge2012_validation_Qle_and_Qh) # L 1
        text_file.write("NSE: %f \n" % -9999) # L 2
        text_file.write("KGEV: %f \n" % -9999) # L 3
        text_file.write("QLEC: %f \n" % kge2012_calibration_Qle) # L 4
        text_file.write("QLEE: %f \n" % kge2012_validation_Qle) # L 5
        text_file.write("QHC: %f \n" % kge2012_calibration_Qh)  # L 6
        text_file.write("QHE: %f \n" % kge2012_validation_Qh) # L 7
        text_file.write("EHC: %f \n" % kge2012_calibration_Qle_and_Qh) # L 8
        text_file.write("EHE: %f \n" % kge2012_validation_Qle_and_Qh) # L 9


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute calibration and validation metrics."
    )

    parser.add_argument(
        "--folder-with-observations",
        required=True,
        help="Path to the folder containing observation data.",
    )

    parser.add_argument(
        "--folder-with-simulations",
        required=True,
        help="Path to the folder containing simulation data.",
    )

    parser.add_argument(
        "--site",
        required=True,
        help="Site identifier.",
    )

    parser.add_argument(
        "--calibration-begining-date",
        required=True,
        help="Calibration start date (e.g. YYYY-MM-DD).",
    )

    parser.add_argument(
        "--calibration-end-date",
        required=True,
        help="Calibration end date (e.g. YYYY-MM-DD).",
    )

    parser.add_argument(
        "--validation-begining-date",
        required=True,
        help="Validation start date (e.g. YYYY-MM-DD).",
    )

    parser.add_argument(
        "--validation-end-date",
        required=True,
        help="Validation end date (e.g. YYYY-MM-DD).",
    )

    args = parser.parse_args()

    compute_metrics(
        folder_with_observations=args.folder_with_observations,
        folder_with_simulations=args.folder_with_simulations,
        site=args.site,
        calibration_begining_date=args.calibration_begining_date,
        calibration_end_date=args.calibration_end_date,
        validation_begining_date=args.validation_begining_date,
        validation_end_date=args.validation_end_date,
    )




