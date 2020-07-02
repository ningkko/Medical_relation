#!/bin/sh
#SBATCH -p priority
#SBATCH -t 2-18:00
#SBATCH —mem=200G
#SBATCH --mail-type=ALL                    # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=yhua@smith.edu   # Email to which notifications will be sent
module load java
python NER_AllArticles_MedScape.py

