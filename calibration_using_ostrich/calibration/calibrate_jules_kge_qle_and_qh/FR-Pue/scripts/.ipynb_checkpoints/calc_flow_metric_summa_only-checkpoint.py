# %%
import xarray as xr
import pandas as pd
import numpy as np
import hydroeval as he

# %%
# read observed Q
obsQ = pd.read_csv('../mizuroute/obsFlow_cms.csv')
obsQ['time'] = pd.to_datetime(obsQ['time'], format='%Y-%m-%d')  # Adjust the format as needed
obsQ= obsQ.set_index('time')
obsQ[obsQ['flow']<0] = np.nan

# %%
# Set date limits for plotting and performance calculations
start_date = pd.to_datetime('1982-10-01')
end_date = pd.to_datetime('1989-09-30')

# %%
# read summa output
summaOutput = xr.open_dataset('summa_results/run1_day.nc')
attr = xr.open_dataset('attributes.nc')
# mizuDomain = xr.open_dataset('mizuroute/topology.nc')
# ixBasinOutlet = np.argwhere(mizuDomain['downSegId'].values <= 0).flatten()

# %%
# read routed flows for the outlet basin
# mizuOutput = xr.open_dataset('mizuroute/mizuroute_results/daily_avg_mizuroute_output.nc')
# Convert the time dimension to only keep the date (remove hours since this is daily average)
summaOutput['time'] = summaOutput['time'].dt.floor('D')

# %%
# extract simulated flows for the basin outlet
simFlow = summaOutput['averageRoutedRunoff_mean'] * attr['HRUarea'].values #.sel(seg=ixBasinOutlet)

# %%
#calculate KGE
KGE = he.evaluator(he.kge, simFlow.sel(time=slice(start_date, end_date)).values, obsQ[start_date:end_date].values)[0][0]

#calculate log NSE
LOG_NSE = he.evaluator(he.nse, simFlow.sel(time=slice(start_date, end_date)).values, obsQ[start_date:end_date].values, transform='log')[0]

NSE = he.evaluator(he.nse, simFlow.sel(time=slice(start_date, end_date)).values, obsQ[start_date:end_date].values)[0]

# %%
# %%
with open("../flow_stats.txt", "w") as text_file:
    text_file.write("KGE: %f \n" % KGE)
    text_file.write("LOG NSE: %f \n" % LOG_NSE)
    text_file.write("NSE: %f \n" % NSE)

# %%



