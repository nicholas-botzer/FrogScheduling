#!/bin/csh
#$ -M nbotzer@nd.edu
#$ -m abe
#$ -q long
#$ -N Simso_Runner_ChromosomesExperiments

module load python/3.6.4

source simsoVirtualProject/simsoVirtual/bin/activate

python3 simulate.py --configFileNames config_2_25_25.xml --resultsFN ./results/br_2_25_25.csv
python3 simulate.py --configFileNames config_2_50_0.xml --resultsFN ./results/br_2_50_0.csv
python3 simulate.py --configFileNames config_2_0_50.xml --resultsFN ./results/br_2_0_50.csv
python3 simulate.py --configFileNames config_4_25_25.xml --resultsFN ./results/br_4_25_25.csv
python3 simulate.py --configFileNames config_4_50_0.xml --resultsFN ./results/br_4_50_0.csv
python3 simulate.py --configFileNames config_4_0_50.xml --resultsFN ./results/br_4_0_50.csv