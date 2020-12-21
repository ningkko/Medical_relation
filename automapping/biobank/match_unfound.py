# Author: Ning
# makiasagawa@gmail.com
import pandas as pd
import tqdm
import subprocess
import json

# loop through cooc, find mpi in pmi dict
print("Matching unfounded...")

i=0
with open(coocfile,'r') as fcooc2:
    pbar2 = tqdm.tqdm(total=n)
    cooc_line2 = fcooc2.readline()
    with open(outputfile,"a") as fout:
        while cooc_line2:

            note1, note2, cooc = cooc_line2.split(",")
            key1 = note1+","+note2
            key2 = note2+","+note1
            if key1 in not_dict:
                fout.write("%s,%s,%s\n" % (key1, not_dict[key1], cooc))
                i+=1
            elif key2 in not_dict:
                fout.write("%s,%s,%s\n" % (key2, not_dict[key2], cooc))
                i+=1
            # pbar2.update(1)
            cooc_line2 = fcooc2.readline()
    fout.close()
fcooc.close()

print("%i out of %i (%f) found."%(i,len(not_dict),i/len(not_dict)))

