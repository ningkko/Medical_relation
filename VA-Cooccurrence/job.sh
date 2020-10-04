#!/bin/sh
#SBATCH -n 1
#SBATCH -c 4
#SBATCH -p short
#SBATCH -t 0-12:00:00
#SBATCH --mem=200G
#SBATCH --mail-type=ALL                 
#SBATCH --mail-user=yhua@smith.edu
python summarize.py
