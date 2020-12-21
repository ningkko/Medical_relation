#!/bin/sh
#SBATCH -p priority
#SBATCH -t 1:30:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL                 
#SBATCH --mail-user=yhua@smith.edu
python map_pos.py