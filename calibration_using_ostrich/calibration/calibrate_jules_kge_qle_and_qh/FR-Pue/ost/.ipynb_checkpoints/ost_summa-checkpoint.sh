#!/bin/bash

echo inside ost_summa Script
# Ensure single-core OpenMP to run parallel mizuRoute in serial mode
# export OMP_NUM_THREADS=1
################################################
############ Inputs ############################
################################################
# specify the common inputs data directory for summa
main_inputs_dir=$(realpath ../../common_inputs)
summa_inputs_dir=$(realpath ../../common_inputs/summa)
mizu_inputs_dir=$(realpath ../../common_inputs/mizuroute)
# specify the summa model directory
SUMMA_exe=$(realpath ../../exes/summa.exe)
# Wouter's version of modified infiltration
# SUMMA_exe=/home/mohamedismaiel.ahmed/comphyd_lab/users/mohamed/SUMMA_diagnostics/summa_inf_wknoben/bin/summa_sundials.exe
# # specify the summa model directory
# mizuRoute_exe=$(realpath ../../exes/mizuRoute.exe)

# copy utilities scripts used to help with calibration
cp -r $(realpath ../../scripts/*.*) ./
cp -r $main_inputs_dir/*.* ./
################################################
###### create directory structure  #############
################################################

### SUMMA
rm -r summa
mkdir -p summa
mkdir -p summa/summa_results/

mv -f calibration_parameters.txt ./summa/
mv -f depth_params.txt ./summa/
# copy summa.exe and inputs
cp -n $SUMMA_exe ./summa/summa.exe
ln -s $summa_inputs_dir/*.* ./summa/

### mizuRoute
rm -r mizuroute/
mkdir -p mizuroute/
mkdir -p mizuroute/mizuroute_results/

# copy files
cp -n $mizuRoute_exe ./mizuroute/mizuRoute.exe
mv -f ./mizuroute.param ./mizuroute/
ln -s $mizu_inputs_dir/*.* ./mizuroute/

################################################
############ SUMMA  ############################
################################################


cd summa

# add the calibrated parameters to the nc file
python ../add_calib_param_trial.py

# add the new depths to the initCond file
python ../add_depth_init_cond.py

# RUN SUMMA
./summa.exe --master fileManager.txt --progress m --version

# get daily average basin total runoff (for faster execution of mizuroute) and delete the first time step (usually it is not a full day)
# note: time should be consistent (especially between the first two time steps to avoid crashes within mizuroute)
# That's why the first timestep is deleted.
# cdo -O -L -delete,timestep=1 -daymean -select,name=basin__TotalRunoff summa_results/myTest_timestep.nc summa_results/daily_avg_totalRunoff.nc

echo SUMMA finished

# calculate metrics for summa runoff only
python ../calc_flow_metric_summa_only.py

# go back to parent directory (Processor_*)
cd ..

# # ################################################
# # #### lumpedSUMMA to distributed mizuRoute  #####
# # ################################################
# # apply lumped SUMMA runoff to all subbasins in the mizuRoute topology file
# python lumpedSUMMA_to_distMizuRoute.py

# # ################################################
# # ############ mizuRoute  ########################
# # ################################################
# # create results directories


# cd mizuroute

# # RUN mizuRoute
# ./mizuRoute.exe mizuroute.control
# # merging all files into one netcdf file and get mean daily value
# # cdo -O -L -mergetime mizuroute_results/run1.* mizuroute_results/daily_avg_mizuroute_output.nc

# echo mizuRoute finished
# # calculate metrics
# python ../calc_flow_metric_summa_mizroute.py
# # go back to root directory
# cd ..

# ################################################
############ flow metrics  #####################
################################################



if [ -f ./flow_stats.txt ]; then
	echo 'Good'
else
  cp bad_flow_stats.txt flow_stats.txt
  echo 'Bad'
fi

pwd
echo ost_summa Script Finished.
