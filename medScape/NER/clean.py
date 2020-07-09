import subprocess
import os
import sys
import shutil
import glob

filepath = '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/MedScape_texts/NER/titles/'
#folders = os.listdir(filepath)
folders = ["mayoclinic/"]

for folder in folders:
    output_file_path = folder.replace("/","")+".txt"
    with open(output_file_path, "a") as output_file:
        output_file.write("Filename|Term|Code|SemanticType|isChemical")
        i = 1
        for file in os.listdir(filepath+folder):
            print(i)
            with open(filepath+folder+file,'r') as f1:
                term = []
                CUI = []
                semanticType = []
                isChemical = []

                info_list = [file]
                
                for line in f1.readlines():
                    if "Term|Code|SemanticType|isChemical" not in line:
                        info = line.split("|")
                        term.append(info[0])
                        CUI.append(info[1])
                        semanticType.append(info[2])
                        isChemical.append(info[3])

                if CUI:
                    info_list.append(",".join(term))
                    info_list.append(",".join(CUI))
                    info_list.append(",".join(semanticType))
                    info_list.append(",".join(isChemical))

                else:
                    info_list += ["NA", "NA", "NA", "NA"]

                output_file.write("|".join(info_list))
            i += 1


        # shutil.rmtree('results')
        # os.mkdir('results')Filename|Term|Code|SemanticType|isChemical