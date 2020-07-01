from utils import *
import sys

import os
files = os.listdir("links/surgery_links/")

i = 0
# each file
for file in files:
    with open("links/surgery_links/" + file) as fp:
        # each url
        url = fp.readline()
        while url:
            
            i+=1
            print(str(i/2945) + "+++++++++++++++++++")
            print("On: " + url)
            get_all_info(url.strip(), type="surgery")

            url = fp.readline()

# print(i)

# test = ["https://emedicine.medscape.com/article/428723-overview",
# "https://emedicine.medscape.com/article/172527-overview",
# "https://emedicine.medscape.com/article/425410-overview",
# "https://emedicine.medscape.com/article/2047916-overview",
# "https://emedicine.medscape.com/article/425698-overview",
# "https://emedicine.medscape.com/article/1193505-overview",
# "https://emedicine.medscape.com/article/798005-overview",
# "https://emedicine.medscape.com/article/1196660-overview",
# "https://emedicine.medscape.com/article/1195680-overview"
# ]


#get_all_info("https://emedicine.medscape.com/article/170066-overview")