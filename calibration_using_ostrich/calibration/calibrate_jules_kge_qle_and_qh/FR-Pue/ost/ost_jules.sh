#!/bin/bash

echo inside ost_jules Script

echo "Host: $(hostname)"
echo "Date: $(date)"


echo "site: ${site}"
echo "metric using ${needed_metric}"
echo "runid: ${runid}"

echo "calibration_begining_date=$calibration_begining_date"
echo "calibration_end_date=$calibration_end_date"
echo "validation_begining_date=$validation_begining_date"
echo "validation_end_date=$validation_end_date"

control_file=../control_step1.txt 
# jules-ok 

# specify the common inputs data directory for summa
main_inputs_dir=$(realpath ../../common_inputs)
jules_inputs_dir=$(realpath ../../common_inputs/jules)
echo "jules_inputs_dir: $jules_inputs_dir"

# copy utilities scripts used to help with calibration
cp -r $(realpath ../../scripts/*.*) ./
cp -r $main_inputs_dir/*.* ./


rm flow_stats.txt
### JULES
rm -r jules
mkdir -p jules
mkdir -p jules/jules_results/
mkdir -p jules/jules_metrics
echo "copying the observations"
cp -r $jules_inputs_dir/observations ./jules/

observations_folder=$(realpath jules/observations)
echo "observations_folder: $observations_folder"


METRICS_DIR=$(realpath jules/jules_metrics)
echo "METRICS DIR: $METRICS_DIR"


mv -f calibration_parameters.txt ./jules/
cp $jules_inputs_dir/*.* ./jules/

# namelist_folder
namelists_folder=$(realpath jules)
PROC_NUM=$(echo "$METRICS_DIR" | sed -n 's/.*Processor_\([0-9]\+\).*/\1/p')
dev_folder1=$namelists_folder/run_model/${PROC_NUM}
echo "dev_folder1: $dev_folder1"
rm -rf $dev_folder1
mkdir -p $dev_folder1
dev_folder2="${dev_folder1}/namelists"
rm -rf $dev_folder2
mkdir -p $dev_folder2
realpath_dev_folder2=$(realpath $dev_folder2)


cd jules
mkdir -p output_files
folder_with_model_results=./output_files 
python ../add_calib_param_trial_jules.py

sed -i "2s|file='soil_frac.txt'|file='${realpath_dev_folder2}/soil_frac.txt'|" ancillaries.nml
sed -i "6s|file='soil_props.txt'|file='${realpath_dev_folder2}/soil_props.txt'|" ancillaries.nml


sed -i "7s|file='${site}_Met.nc'|file='${realpath_dev_folder2}/${site}_Met.nc'|" drive.nml

sed -i "8s|file='${site}_lai_pft.nc'|file='${realpath_dev_folder2}/${site}_lai_pft.nc'|" prescribed_data.nml


cp -r * $dev_folder2/


### devbox start


cd . 
EXAMPLE_DIR=$dev_folder1

EXAMPLE_DIR="$EXAMPLE_DIR" nix-user-chroot /home/users/$USER/.nix bash -lc '
  set -euo pipefail
  export DEVBOX_NO_PROMPT=1
  export PATH=/home/users/'"$USER"'/.local/bin:$PATH

  unset LD_LIBRARY_PATH
  unset PYTHONPATH
  export PYTHONNOUSERSITE=1

  source /home/users/'"$USER"'/.nix-profile/etc/profile.d/nix.sh
  cd "$EXAMPLE_DIR"
  echo "Current directory: $(pwd)"
  devbox run -c /home/users/'"$USER"'/soft/portable-jules/devbox.json jules -n namelists "$(pwd)"
'
# Check the output files 
ls -la ${dev_folder1}/output_files/

cp -r ${dev_folder1}/output_files/* $folder_with_model_results/
# devbox end 


echo JULES finished
cd $namelists_folder

current_location=$(pwd)
echo "Current location: $current_location"
cd $folder_with_model_results
mkdir -p dump_files
cp *.dump.* dump_files/
rm -rf *dump*
cd $namelists_folder


python ../metrics_clean_before.py --metrics_folder $METRICS_DIR # ok with jules 


python ../calculate_metrics_from_jules.py --folder-with-observations $observations_folder --folder-with-simulations $folder_with_model_results --site $site --calibration-begining-date $calibration_begining_date --calibration-end-date $calibration_end_date --validation-begining-date $validation_begining_date --validation-end-date $validation_end_date


python ../save_current_run.py --base_folder $scratch_path --output_folder $save_folder # new


cd ..


if [ -f ./flow_stats.txt ]; then
	echo 'Good'
else
  cp bad_flow_stats.txt flow_stats.txt
  echo 'Bad'
fi

pwd
echo ost_jules Script Finished.
