#$ -S /bin/bash
# [jules ready]

echo "Clean previous run files"


# rm slurm-*.out

rm -r exes

rm OstOutput0.txt dds_status.out 
rm -r best_run/
rm -r paramSet_objFun/
rm -r paramSet_objFun.tar

cd ost
rm -rf Processor_*
rm OstModel*.txt
rm OstOutput*.txt
rm OstTemp_*.txt
rm -rf OstErrors*.txt
rm -rf dds_status.out OstDDSPn.txt OstStatus0.txt
rm OstrichMPI
