#!/bin/csh
#$ -M yzhang46@nd.edu
#$ -m abe
#$ -q long
#$ -N Simso_Runner_ChromosomesExperiments

module load python/3.6.4
python --version
pwd
python3 ../simulate.py --configFileNames baseTest.xml --schedNames FROG.py --numGen 50 --numChrom 100 -ESC .1 .4 .5 --mutRate .75 --resultsFN test.csv --pklFileName test.pkl 

deactivate
