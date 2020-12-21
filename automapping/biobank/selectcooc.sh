#!/bin/sh
#SBATCH -n 1
#SBATCH -p priority
#SBATCH -t 0-18:00
#SBATCH --mem=200G
#SBATCH --mail-type=ALL                 
#SBATCH --mail-user=yhua@smith.edu
python selectcooc.py

