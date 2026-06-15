#!/bin/bash
# [jules_ready]
# FILENAME:  ostrich.sh

#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --partition=standard
#SBATCH --qos=high
#SBATCH --mem-per-cpu=5GB
#SBATCH --cpus-per-task=1
#SBATCH --account=account_name_in_jasmin
#SBATCH --time=23:59:00
#SBATCH --job-name=ostrich
#SBATCH --mail-user=user@company.ca
#SBATCH --mail-type=ALL
#SBATCH --output=./logs/slurm-output/slurm-%A_%a.out
#SBATCH --error=./logs/slurm-error/slurm-%A_%a.out

# to test scripts debug debug 
# then standard and high
#------------------------------------------------------ # 
echo "****************************************************"
echo "Parallel job started at: `date`"


site="FR-Pue"
needed_metric="kge_qleqh"
runid="run2500ga1"

calibration_begining_date="2000-01-01"
calibration_end_date="2004-12-31"
validation_begining_date="2005-01-01"
validation_end_date="2015-01-01"


scratch_path=/work/scratch-pw4/$USER/ostrich_scratch/calibration_ostrich/$SLURM_JOBID/${runid}/${needed_metric}/${site} 
save_folder=/home/users/$USER/ostrich_data/${runid}/${needed_metric}/${site} #new
ostrich_exe=/home/users/$USER/software/Ostrich_v17.12.19c/OstrichMPI

export site
export needed_metric
export runid

mkdir -p $scratch_path
export scratch_path
echo $scratch_path
mkdir -p $save_folder # new
export save_folder # new
export calibration_begining_date
export calibration_end_date
export validation_begining_date
export validation_end_date


module load oneapi/compilers/24.2.0
module load oneapi/mpi/24.2.0
module load netcdf/intel2024.2.0/4.9.2
module load netcdf/intel2024.2.0/fortran/4.6.1
export HDF5_LIBDIR=/apps/jasmin/supported/libs/hdf5/intel2024.2.0/1.14.4-2/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_LIBDIR
export NETCDF_FORTRAN_ROOT=/apps/jasmin/supported/libs/netcdf/intel2024.2.0/fortran/4.6.1
module unload jaspy
source ~/miniforge3/bin/activate
eval "$(mamba shell hook --shell bash)"
mamba activate /home/users/iaguirre/python-envs/conda/pl2_jules_v2

export PYTHONNOUSERSITE=1
unset PYTHONPATH


####################
# clean previous run files
./clean.sh
####################
# specify exe locations (full paths)

chmod +x $ostrich_exe

# put the exes in a folder
mkdir -p exes

origin_path=$(pwd)
cp -r $ostrich_exe ${origin_path}/ost/OstrichMPI
chmod +x ${origin_path}/ost/OstrichMPI

###################
# copy entire setup from origin to the scratch directory (destination)
origin_path=$(pwd)
echo $scratch_path
mkdir -p "$scratch_path"
cp -a "$origin_path/." "$scratch_path/"


cd $scratch_path/ost
chmod +x OstrichMPI
chmod -R +x $scratch_path

export I_MPI_PMI_LIBRARY=/lib64/libpmi2.so
export I_MPI_DEBUG=5

srun --mpi=pmi2 -n $SLURM_NTASKS ./OstrichMPI


cd ..
python scripts/save_current_run.py --base_folder $scratch_path --output_folder $save_folder # new


# post-processing
# clean everything to save space on scratch, only if the run is successful
# copy run files
if [ -f $scratch_path/ost/Processor_0/flow_stats.txt ]; then
    echo "Run was succesful"
    fi
else
    # no flow_stats.txt in Processor_0, run terminated either due to timelimit or other reasons
    echo "run failed"
    echo "run terminated either due to timelimit or other reasons"
fi
echo "Parallel job finished with exit code $? at: `date`"
echo "****************************************************"
