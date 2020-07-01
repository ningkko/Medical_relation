from utils import *
import sys

import os
files = os.listdir("links/pediatrics_links/")

# each file
for file in files:
    with open("links/pediatrics_links/" + file) as fp:
        # each url
        url = fp.readline()
        while url:
            get_all_info(url.strip(), type="pediatrics")

            url = fp.readline()


files = os.listdir("links/surgery_links/")

for file in files:
    with open("links/surgery_links/" + file) as fp:
        # each url
        url = fp.readline()
        while url:
            
            get_all_info(url.strip(), type="surgery")

            url = fp.readline()
