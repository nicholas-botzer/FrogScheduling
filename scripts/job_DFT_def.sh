#!/bin/csh
#$ -M yzhang46@nd.edu
#$ -m bes
#$ -q long
#$ -N Simso_Runner_ChromosomesExperiments


python3 simulate.py --configFileNames config_2_25_25.xml --resultsFN draftFT_def.csv

