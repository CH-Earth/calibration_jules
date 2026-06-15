# %%
print('inside the add_calib_param_trial.py')

# %%
import xarray as xr

# %%
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
            if line.startswith('#') or not line.strip():
                continue
            # Split the line into components based on the delimiter '|'
            parts = line.split('|')
            # Extract the parameter name, dimension, and values, and strip any extra spaces
            parameter_name = parts[0].strip()
            dimension = parts[1].strip()
            values = [float(val.strip()) for val in parts[2].strip().split(',')]
            # Store the values in the dictionary
            parameter_values[parameter_name] = {'dimension': dimension, 'values': values}
    
    return(parameter_values)

# %%
parameter_values = read_calibration_parameters_txt()

# %%
par_trial = xr.open_dataset('trialParams.priori.nc')

# %%
for name,dim_val in parameter_values.items():
    # print('name', name)
    # print('value', dim_val['dimension'])
    # add soil parameters (most sensitive is k_soil)
    par_trial[name] = xr.DataArray(dim_val['values'], dims=(dim_val['dimension']))

par_trial.to_netcdf('trialParams.nc')

par_trial

# %%



