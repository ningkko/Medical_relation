from utils import *
import sys

import os
files = os.listdir("surgery_links/")

i = 0
# each file
for file in files:
    with open("surgery_links/" + file) as fp:
        # each url
        url = fp.readline()
        while url:
            
            i+=1
            # print(str(i/2945) + "+++++++++++++++++++")
            # print("On: " + url)
            # get_all_info(url.strip(), type="surgery")

            url = fp.readline()

print(i)
