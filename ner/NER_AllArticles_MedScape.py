import subprocess
import os
import sys
import shutil
import glob

filepath = '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/MedScape_texts/'
folders = ['medicine_txts/', 'pediatrics_txts/', 'surgery_txts/']

for folder in folders:
    for file in os.listdir(filepath+folder):
        if file not in os.listdir(filepath + "NER/" + folder):
            print(file)
            fn1 = open(filepath+folder+file,'r')
            f1 = open('articles/Articles.txt','w')
            for x in fn1.readlines():
                f1.write(x)
            fn1.close()
            f1.close()
            os.system("sh runMiniNERAllInOne.sh")
            shutil.copy('results/NER_output.txt', filepath + "NER/" + folder + file)
        # shutil.rmtree('results')
        # os.mkdir('results')
#!/bin/sh
#SBATCH -p priority
#SBATCH -t 2-18:00
#SBATCH —mem=200G
#SBATCH --mail-type=ALL                    # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=yhua@smith.edu   # Email to which notifications will be sent
module load java
python NER_AllArticles_MedScape.py

import subprocess
import os
import sys
import shutil
import glob

filepath = '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/MedScape_texts/'
folders = ['medicine_txts/', 'pediatrics_txts/', 'surgery_txts/']

for folder in folders:
    for file in os.listdir(filepath+folder):
        if file not in os.listdir(filepath + "NER/" + folder):
            print(file)
            fn1 = open(filepath+folder+file,'r')
            f1 = open('articles/Articles.txt','w')
            for x in fn1.readlines():
                f1.write(x)
            fn1.close()
            f1.close()
            os.system("sh runMiniNERAllInOne.sh")
            shutil.copy('results/NER_output.txt', filepath + "NER/" + folder + file)
        # shutil.rmtree('results')
        # os.mkdir('results')
