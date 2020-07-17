import subprocess
import os
import sys
import shutil
import glob

filepath = '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/MedScape_texts/NER/titles/'
#folders = os.listdir(filepath)
folders = ['medicine_txts/', 'medlineplus/', 'mSDManual/', 'pediatrics_txts/', 'surgery_txts/', 'wikipedia/']
for folder in folders:
    output_file_path = folder.replace("/","")+".txt"
    with open("cui_phe/source/"+output_file_path, "w") as output_file:
        output_file.write("Filename|Term|Code|SemanticType|isChemical\n")
        i = 1
        files = os.listdir(filepath+folder)
        files.sort()

        for file in files:
            # print("%f: %s" %(i/197877, file))
                
            with open(filepath+folder+file,'r') as f1:
                term = []
                CUI = []
                semanticType = []
                isChemical = []

                info_list = [file, "NA", "NA", "NA", "NA"]
                
                for line in f1.readlines():
                    if "Term|Code|SemanticType|isChemical" not in line:
                        info = line.split("|")
                        if len(info) == 4:
                            term.append(info[0])
                            CUI.append(info[1])
                            semanticType.append(info[2])
                            isChemical.append(info[3].replace("\n",""))

                            if CUI:
                                # print(file)
                                info_list = [file, ",".join(term), ",".join(CUI), ",".join(semanticType), ",".join(isChemical)]

                output_file.write("|".join(info_list))
                output_file.write("\n")
            i += 1


        # shutil.rmtree('results')
        # os.mkdir('results')Filename|Term|Code|SemanticType|isChemical
