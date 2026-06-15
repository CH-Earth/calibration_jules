# calibration parameters to be added to the paramTrial nc file
# parameter name                | dimension (hru or gru) | values comma separated
# must be same name as in summa |   (hru or gru)         | (per gru/hru)
#--------------------------------------------------------------------------------
k_soil	            |	hru	|	_k_soil_
theta_sat	        |	hru	|	_theta_sat_
aquiferBaseflowExp	|	hru	|	_aquiferBaseflowExp_
aquiferBaseflowRate	|	hru	|	_aquiferBaseflowRate_
qSurfScale	        |	hru	|	_qSurfScale_
frozenPrecipMultip	|	hru	|	_frozenPrecipMultip_
heightCanopyBottom	|	hru	|	_heightCanopyBottom_
heightCanopyTop	    |	hru	|	_heightCanopyTop_
Fcapil	            |	hru	|	_Fcapil_
tempCritRain	    |	hru	|	_tempCritRain_
windReductionParam	|	hru	|	_windReductionParam_
vGn_n	            |	hru	|	_vGn_n_
# macropore related parameters do not improve KGE for streamflow
k_macropore         |   hru |   _k_macropore_
theta_mp            |   hru |   _theta_mp_
# snow related parameters (senstivie params for snow simulation)
albedoMax           |	hru	|	_albedoMax_
albedoRefresh       |	hru	|	_albedoRefresh_
albedoDecayRate     |	hru	|	_albedoDecayRate_
albedoMinSpring     |	hru	|	_albedoMinSpring_
mw_exp              |	hru	|	_mw_exp_
z0Snow              |	hru	|	_z0Snow_
leafExchangeCoeff   |	hru	|	_leafExchangeCoeff_
leafDimension       |	hru	|	_leafDimension_
# hillslope routing
routingGammaShape   |   gru |   _routingGammaShape_
routingGammaScale   |   gru |   _routingGammaScale_
##########################
## multiplier section
## leave uncommented
## not used by the script or model (used for sanity checks)
##########################
## thetamp_multiplier    | _thetamp_multp_
## kmacropore_multipier  | _kmacropore_multp_
## heightCanopyTop_multp | _hghtCnpyTop_multp_