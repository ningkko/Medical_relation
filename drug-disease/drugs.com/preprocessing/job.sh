#!/bin/bash
#SBATCH -c 4                               # Request one core
#SBATCH -N 1                               # Request one node (if you request more than one core with -c, also using
                                           # -N 1 means all cores will be on the same node)
#SBATCH -t 0-24:00                         # Runtime in D-HH:MM format
#SBATCH -p priority                        # Partition to run in
#SBATCH --mem=160G                          # Memory total in MB (for all cores)
#SBATCH --mail-type=ALL                    # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=yhua@smith.edu   # Email to which notifications will be sent
python scrape.py
