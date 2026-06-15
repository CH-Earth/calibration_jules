#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xarray as xr
import numpy as np
import pandas as pd


# In[2]:


# adapted from CONFLUENCE: https://github.com/DarriEy/CONFLUENCE/blob/main/utils/optimization/de_optimizer.py
# The soil depth calibration uses two parameters:
#     - total_mult: Overall depth multiplier (0.1-5.0)
#     - shape_factor: Controls depth profile shape (0.1-3.0)
#       - shape_factor > 1: Deeper layers get proportionally thicker
#       - shape_factor < 1: Shallower layers get proportionally thicker
#       - shape_factor = 1: Uniform scaling


# In[3]:


# Read the text file with '|' as delimiter and '#' as comment indicator
df = pd.read_csv('depth_params.txt', sep='|', comment='#', header=None)


# In[6]:


# parameters
total_mult = df[1][0]
shape_factor = df[1][1]


# In[2]:


init_cond = xr.open_dataset('coldState.priori.nc')


# In[25]:


# soil depth has to be 8
soil_mLayerDepth= init_cond['mLayerDepth'].squeeze().values
soil_mLayerDepth


# In[27]:
# calculate the new depths

# arr = self.original_depths.copy()
n = len(soil_mLayerDepth)
idx = np.arange(n)

# Calculate shape weights
if shape_factor > 1:
    # Deeper layers get proportionally thicker
    w = np.exp(idx / (n - 1) * np.log(shape_factor))
elif shape_factor < 1:
    # Shallower layers get proportionally thicker
    w = np.exp((n - 1 - idx) / (n - 1) * np.log(1 / shape_factor))
else:
    # Uniform scaling
    w = np.ones(n)

# Normalize weights to preserve total depth scaling
w /= w.mean()

# sort the weights to be from smallest to largest
w = np.sort(w)

# Apply total multiplier and shape weights
new_depths = soil_mLayerDepth * w * total_mult
new_depths


# In[28]:


# init_cond['nSoil'] = xr.DataArray([[len(soil_mLayerDepth)]] , dims=('scalarv', 'hru'))
init_cond['iLayerHeight'] = xr.DataArray(np.transpose([[0]+list(np.cumsum(new_depths))]) , dims=('ifcToto', 'hru'))
init_cond['mLayerDepth'] = xr.DataArray(np.transpose([new_depths]), dims=('midToto',  'hru'))
init_cond.to_netcdf('coldState.nc')

