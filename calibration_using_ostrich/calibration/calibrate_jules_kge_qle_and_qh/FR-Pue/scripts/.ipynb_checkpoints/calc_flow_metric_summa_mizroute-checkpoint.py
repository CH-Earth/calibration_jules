# calculate flow metrics for mizuRoute routed output
# %%
import xarray as xr
import pandas as pd
import numpy as np
import hydroeval as he

# %%
# read observed Q
obsQ = pd.read_csv('obsFlow_cms.csv')
obsQ['time'] = pd.to_datetime(obsQ['time'], format='%Y-%m-%d')  # Adjust the format as needed
obsQ= obsQ.set_index('time')
obsQ[obsQ['flow']<0] = np.nan

# %%
# Set date limits for plotting and performance calculations
start_date = pd.to_datetime('1982-10-01')
end_date = pd.to_datetime('1989-09-30')

# %%
# read mizuroute domain to get the location of the outlet basin
mizuDomain = xr.open_dataset('topology.nc')
ixBasinOutlet = np.argwhere(mizuDomain['downSegId'].values <= 0).flatten()

# %%
# read routed flows for the outlet basin
mizuOutput = xr.open_dataset('mizuroute_results/run1.h.1981-10-02-00000.nc')
# Convert the time dimension to only keep the date (remove hours since this is daily average)
mizuOutput['time'] = mizuOutput['time'].dt.floor('D')

# %%
# extract simulated flows for the basin outlet
simFlow = mizuOutput['IRFroutedRunoff'].sel(seg=ixBasinOutlet)

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



