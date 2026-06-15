#!/usr/bin/env python
# coding: utf-8

# In[12]:


import xarray as xr
import pandas as pd
import numpy as np
import os
import netCDF4 as nc4

# In[3]:


summa_output = xr.open_dataset('summa/summa_results/run1_day.nc')
summa_output.load()


# # mizuRoute topology
# 

# In[4]:


mizuTopology = xr.open_dataset('mizuroute/topology.nc')
mizuTopology.load()


# # create mizuRoute forcing
# use lumped summa output and assign it to all subbasins in the mizuRoute topology

# In[24]:


mizuForcing = xr.Dataset()
# prepare for the summa attr file
mizuForcing ['time']          = xr.DataArray(summa_output['time'], dims=('time'))
mizuForcing ['gru']          = xr.DataArray(mizuTopology['segId'].values.flatten(), dims=('gru'), 
                                        attrs={'long_name': 'Index of GRU', 'units': '-'})

mizuForcing ['gruId'] = xr.DataArray(mizuTopology['segId'].values.flatten(), dims=('gru'))

mizuForcing ['basin__TotalRunoff_mean']    = xr.DataArray(np.tile(summa_output['basin__TotalRunoff_mean'].values, (1, len(mizuTopology['segId'].values.flatten()))),  # shape: (time, n_repeat)
                                                 dims=('time','gru'), 
                                                attrs={'long_name': 'daily instant total runoff', 'units': 'm/s'})

mizuForcing ['averageRoutedRunoff_mean']    = xr.DataArray(np.tile(summa_output['averageRoutedRunoff_mean'].values, (1, len(mizuTopology['segId'].values.flatten()))),  # shape: (time, n_repeat)
                                                 dims=('time','gru'), 
                                                attrs={'long_name': 'daily routed total runoff', 'units': 'm/s'})

        # 'basin__TotalRunoff_mean': repeated_total,
        # 'averageRoutedRunoff_mean': repeated_routed
mizuForcing.to_netcdf('summa/summa_results/run1_day_mizuForcing.nc')
mizuForcing.close()

# In[25]:


# replace T in the time unit with space

ncid = nc4.Dataset('summa/summa_results/run1_day_mizuForcing.nc', 'r+')

# Access the 'units' attribute and replace 'T' with a space
units_attribute = ncid['time'].units
units_attribute = units_attribute.replace('T', ' ')

# Update the 'units' attribute in the netCDF file
ncid['time'].setncattr('units', units_attribute)

# Close the netCDF file
ncid.close()


# In[ ]:





# In[ ]:




