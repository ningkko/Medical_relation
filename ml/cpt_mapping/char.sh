#!/bin/sh
#SBATCH -p priority
#SBATCH -t 1-12:00
#SBATCH --mem=200
#SBATCH --mail-type=ALL                 
#SBATCH --mail-user=yhua@smith.edu
python char.py