# JULES Calibration Scripts

> Developed by **Ignacio Aguirre**  
> 📧 [ignacio.aguirre@ucalgary.ca](mailto:ignacio.aguirre@ucalgary.ca)

## Calibration of Flux Towers in JULES Using Ostrich

This repository contains scripts and workflows for calibrating **JULES (Joint UK Land Environment Simulator)** against flux tower observations using the **Ostrich optimization framework**.

After installing all the packages, to run the optimization, submit the key shell file:

```
sbatch submit_job.sh
```

The following lines are critical:

```
site="FR-Pue"
needed_metric="kge_qleqh"
runid="run2500ga1"

calibration_begining_date="2000-01-01"
calibration_end_date="2004-12-31"
validation_begining_date="2005-01-01"
validation_end_date="2015-01-01"

# where the model is going to run (in scratch)
scratch_path=/work/scratch-pw4/$USER/ostrich_scratch/calibration_ostrich/$SLURM_JOBID/${runid}/${needed_metric}/${site} 
# where to save the files with parameters
save_folder=/home/users/$USER/ostrich_data/${runid}/${needed_metric}/${site} #new
# the path to Ostrich
ostrich_exe=/home/users/$USER/software/Ostrich_v17.12.19c/OstrichMPI
```

Also, remember to check the sbatch lines. 

You can leave the ram, nodes, and tasks fixed, but the account, email, and path for the output and errors files must be modified. 

```
#SBATCH --nodes=1 
#SBATCH --ntasks=10
#SBATCH --partition=standard
#SBATCH --qos=high
#SBATCH --mem-per-cpu=5GB
#SBATCH --cpus-per-task=1
#SBATCH --account=account_name_in_jasmin
#SBATCH --time=23:59:00
#SBATCH --job-name=ostrich
#SBATCH --mail-user=ignacio.aguirre@ucalgary.ca
#SBATCH --mail-type=ALL
#SBATCH --output=/work/scratch-pw4/iaguirre/plumber_running/logs/slurm-output/slurm-%A_%a.out
#SBATCH --error=/work/scratch-pw4/iaguirre/plumber_running/logs/slurm-error/slurm-%A_%a.out

```

Happy coding!