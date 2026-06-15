print('inside the JULES add_calib_param_trial.py')

import pandas as pd
import shutil
from pathlib import Path
import re 
import os 

def vcrit_equation(vsat, sathh, b):
    parenthesis1 = (sathh / 3.364)
    parenthesis2 = (parenthesis1) ** (1 / b)
    parenthesis3 = vsat * parenthesis2
    return parenthesis3

def vwilt_equation(vsat,sathh, b):
    parenthesis1 = (sathh / 152.9)
    parenthesis2 = (parenthesis1) ** (1 / b)
    parenthesis3 = vsat * parenthesis2
    return parenthesis3


def update_soil_props(file_path, updates):
    """
    Read a soil_props.txt file, replace values based on `updates`,
    and create a backup copy before modifying.

    Parameters
    ----------
    file_path : str or Path
        Path to soil_props.txt
    updates : dict
        Dictionary with keys as variable names (e.g., {"b": 5})
        and values as replacements
    """

    file_path = Path(file_path)
    backup_path = file_path.with_suffix(file_path.suffix + ".ori")

    # Define headers
    headers = [
        "b", "hcap", "sm_wilt", "hcon", "sm_crit",
        "satcon", "sathh", "sm_sat", "albsoil"
    ]

    # Create backup if it doesn't exist
    if not backup_path.exists():
        shutil.copy(file_path, backup_path)

    # Read data
    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        header=None,
        names=headers
    )

    # Apply updates
    for key, value in updates.items():
        if key not in df.columns:
            raise KeyError(f"'{key}' is not a valid soil property")
        df.loc[0, key] = value

    # Write back to file (space-separated, no header/index)
    df.to_csv(
        file_path,
        sep=" ",
        header=False,
        index=False,
        float_format="%.8g"
    )



def update_pft_params_nml(file_path, row_multipliers):
    _NUM = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"

    """
    Multiply values for specified namelist variables.
    - For tokens like '6*0.005', multiplies ONLY 0.005 (never the 6).
    - For plain numbers like '0.78', multiplies the number.
    - Preserves commas, whitespace, and line breaks.
    - Creates backup file_path.ori (only if it doesn't already exist).
    """
    file_path = Path(file_path)
    backup_path = file_path.with_suffix(file_path.suffix + ".ori")
    if not backup_path.exists():
        shutil.copy(file_path, backup_path)

    text = file_path.read_text(encoding="utf-8")

    def to_float(s: str) -> float:
        return float(s.replace("D", "E").replace("d", "e"))

    def format_like(original: str, value: float) -> str:
        # compact, but keeps D exponent if original used D/d
        out = f"{value:.12g}"
        if "D" in original.upper():
            out = re.sub(r"[Ee]", "D", out)
        return out

    # Repeat token: n * value  (capture prefix separately so we never touch n)
    repeat_token_re = re.compile(rf"^(\s*\d+\s*\*\s*)({_NUM})(\s*)$")

    # Plain number token
    num_token_re = re.compile(rf"^(\s*)({_NUM})(\s*)$")

    for var, factor in row_multipliers.items():
        factor = float(factor)

        # Find the assignment start for var
        m = re.search(rf"(?m)^\s*{re.escape(var)}\s*=", text)
        if not m:
            raise KeyError(f"Variable '{var}' not found in {file_path.name}")

        start = m.start()

        # End at next assignment OR "/" OR new "&group"
        m_next = re.search(r"(?m)^\s*(?:[A-Za-z_]\w*\s*=|/|&\w+)", text[m.end():])
        end = (m.end() + m_next.start()) if m_next else len(text)

        block = text[start:end]
        lhs, rhs = block.split("=", 1)

        # Split RHS into tokens, keeping commas
        parts = re.split(r"(,)", rhs)

        for i, part in enumerate(parts):
            if part == ",":
                continue

            mr = repeat_token_re.match(part)
            if mr:
                prefix, v_str, suffix = mr.group(1), mr.group(2), mr.group(3)
                new_v = to_float(v_str) * factor
                parts[i] = prefix + format_like(v_str, new_v) + suffix
                continue

            mn = num_token_re.match(part)
            if mn:
                prefix, v_str, suffix = mn.group(1), mn.group(2), mn.group(3)
                new_v = to_float(v_str) * factor
                parts[i] = prefix + format_like(v_str, new_v) + suffix
                continue

            # else: leave unchanged (comments/blank/etc.)

        new_rhs = "".join(parts)
        new_block = lhs + "=" + new_rhs
        text = text[:start] + new_block + text[end:]

    file_path.write_text(text, encoding="utf-8")


def update_pft_params_nml_replace_not_multiply(file_path, row_multipliers):
    _NUM = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"

    """
    Multiply values for specified namelist variables.
    - For tokens like '6*0.005', multiplies ONLY 0.005 (never the 6).
    - For plain numbers like '0.78', multiplies the number.
    - Preserves commas, whitespace, and line breaks.
    - Creates backup file_path.ori (only if it doesn't already exist).
    """
    file_path = Path(file_path)
    backup_path = file_path.with_suffix(file_path.suffix + ".ori")
    if not backup_path.exists():
        shutil.copy(file_path, backup_path)

    text = file_path.read_text(encoding="utf-8")

    def to_float(s: str) -> float:
        return float(s.replace("D", "E").replace("d", "e"))

    def format_like(original: str, value: float) -> str:
        # compact, but keeps D exponent if original used D/d
        out = f"{value:.12g}"
        if "D" in original.upper():
            out = re.sub(r"[Ee]", "D", out)
        return out

    # Repeat token: n * value  (capture prefix separately so we never touch n)
    repeat_token_re = re.compile(rf"^(\s*\d+\s*\*\s*)({_NUM})(\s*)$")

    # Plain number token
    num_token_re = re.compile(rf"^(\s*)({_NUM})(\s*)$")

    for var, factor in row_multipliers.items():
        factor = float(factor)

        # Find the assignment start for var
        m = re.search(rf"(?m)^\s*{re.escape(var)}\s*=", text)
        if not m:
            raise KeyError(f"Variable '{var}' not found in {file_path.name}")

        start = m.start()

        # End at next assignment OR "/" OR new "&group"
        m_next = re.search(r"(?m)^\s*(?:[A-Za-z_]\w*\s*=|/|&\w+)", text[m.end():])
        end = (m.end() + m_next.start()) if m_next else len(text)

        block = text[start:end]
        lhs, rhs = block.split("=", 1)

        # Split RHS into tokens, keeping commas
        parts = re.split(r"(,)", rhs)

        for i, part in enumerate(parts):
            if part == ",":
                continue

            mr = repeat_token_re.match(part)
            if mr:
                prefix, v_str, suffix = mr.group(1), mr.group(2), mr.group(3)
                new_v = (to_float(v_str)*0) + factor
                parts[i] = prefix + format_like(v_str, new_v) + suffix
                continue

            mn = num_token_re.match(part)
            if mn:
                prefix, v_str, suffix = mn.group(1), mn.group(2), mn.group(3)
                new_v = (to_float(v_str)*0) + factor
                parts[i] = prefix + format_like(v_str, new_v) + suffix
                continue

            # else: leave unchanged (comments/blank/etc.)

        new_rhs = "".join(parts)
        new_block = lhs + "=" + new_rhs
        text = text[:start] + new_block + text[end:]

    file_path.write_text(text, encoding="utf-8")


def read_calibration_parameters_txt():
    # read the parameters from the text file
    # Define the input and output file names
    input_file = 'calibration_parameters.txt'

    # Initialize an empty dictionary to store the parameter values
    parameter_values = {}

    # Open the file and read its contents
    with open(input_file, 'r') as file:
        # Read the file line by line
        for line in file:
            # Skip lines that are comments or empty
            if line.startswith('#') or not line.strip(): # if the word multp_ is in the line, skip it
                continue
            if 'multp' in line or "frac" in line or "offset" in line or "range" in line: # skip lines with multipliers or fractions
                continue
            # Split the line into components based on the delimiter '|'
            parts = line.split('|')
            # Extract the parameter name, dimension, and values, and strip any extra spaces
            parameter_name = parts[0].strip()
            dimension = parts[1].strip()
            values = [float(val.strip()) for val in parts[2].strip().split(',')]
            print (f"parameter_name: {parameter_name}, dimension: {dimension}, values: {values}")

            # Store the values in the dictionary
            parameter_values[parameter_name] = {'dimension': dimension, 'values': values}
    
    return(parameter_values)


parameter_values = read_calibration_parameters_txt()

vcrit_value = vcrit_equation(parameter_values['sm_sat']['values'][0], parameter_values['sathh']['values'][0], parameter_values['b']['values'][0])
print(f"vcrit_value: {vcrit_value}")
vwilt_value = vwilt_equation(parameter_values['sm_sat']['values'][0], parameter_values['sathh']['values'][0], parameter_values['b']['values'][0])
print(f"vwilt_value: {vwilt_value}")

vsat_value = parameter_values['sm_sat']['values'][0]
condition1 = vsat_value > vcrit_value
condition2 = vcrit_value > vwilt_value
print(f"condition1: {condition1}, condition2: {condition2}")

parameter_values['sm_crit'] = {'dimension': 'hru', 'values': [vcrit_value]}
print(f"Added sm_crit with value: {parameter_values['sm_crit']['values'][0]}")
parameter_values['sm_wilt'] = {'dimension': 'hru', 'values': [vwilt_value]}
print(f"Added sm_wilt with value: {parameter_values['sm_wilt']['values'][0]}")

current_path = os.getcwd()
print(f"current_path inside add_calib_param_trial.py: {current_path}")
soil_parameters = [
        "b", "hcap", "sm_wilt", "hcon", "sm_crit",
        "satcon", "sathh", "sm_sat", "albsoil"
    ]

pft_veg_parameters  = [
    "a_wl_io",
    "a_ws_io",
    "albsnc_max_io",
    "albsnc_min_io",
    "alnir_io",
    "alpar_io",
    "alpha_io",
    "b_wl_io",
    "c3_io",
    "can_struct_a_io",
    "canht_ft_io",
    "dgl_dm_io",
    "dgl_dt_io",
    "dqcrit_io",
    "emis_pft_io",
    "eta_sl_io",
    "f0_io",
    "fd_io",
    "fsmc_mod_io",
    "fsmc_of_io",
    "fsmc_p0_io",
    "g_leaf_0_io",
    "glmin_io",
    "gsoil_f_io",
    "infil_f_io",
    "kext_io",
    "kn_io",
    "knl_io",
    "kpar_io",
    "lai_alb_lim_io",
    "lai_io",
    "neff_io",
    "nl0_io",
    "nr_nl_io",
    "ns_nl_io",
    "omega_io",
    "omnir_io",
    "orient_io",
    "q10_leaf_io",
    "r_grow_io",
    "sigl_io",
    "tleaf_of_io",
    "tlow_io",
    "tupp_io",
    "z0hm_classic_pft_io",
    "z0v_io",
]

pft_replace = ["z0hm_pft_io", "catch0_io",  "dcatch_dlai_io", "rootd_ft_io"]

snow_parameters = ["n_lai_exposed"]

for name,dim_val in parameter_values.items():
    # print('name', name)
    # print('value', dim_val['dimension'])
    # add soil parameters (most sensitive is k_soil)
    if name in soil_parameters:
        print(f"Adding soil parameter: {name}")
        # add to soil_props.txt
        file_path = os.path.join(current_path, "soil_props.txt")
        updates = {
            name: dim_val['values'][0]}  # take the first value
        update_soil_props(file_path, updates)
    
    if name in pft_veg_parameters:
        print(f"Adding pft_veg parameter: {name}")
        # add to pft_params.nml
        pft_file = os.path.join(current_path, "pft_params.nml")
        update_pft = {name: dim_val['values'][0]}  # take the first value
        update_pft_params_nml(pft_file, update_pft)
    
    if name in snow_parameters:
        print(f"Adding snow parameter: {name}")
        # add to snow_params.nml
        snow_file = os.path.join(current_path, "jules_snow.nml")
        update_snow = {name: dim_val['values'][0]}  # take the first value
        update_pft_params_nml(snow_file, update_snow)
    
    if name in pft_replace:
        print(f"Adding pft_replace parameter: {name}")
        # add to pft_params.nml
        pft_file = os.path.join(current_path, "pft_params.nml")
        update_pft = {name: dim_val['values'][0]}  # take the first value
        update_pft_params_nml_replace_not_multiply(pft_file, update_pft)