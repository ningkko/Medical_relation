from utils import *
import sys

import os
files = os.listdir("medicine_links")

i = 0
# each file
for file in files:
	with open("medicine_links/" + file) as fp:
		# each url
		url = fp.readline()
		while url:
			
			i+=1
			print(str(i/7887) + "+++++++++++++++++++")
			print("On: " + url)
			get_all_info(url.strip())

			url = fp.readline()

# test = ["https://emedicine.medscape.com/article/135478-overview",
#         "https://emedicine.medscape.com/article/285433-overview",
#         "https://emedicine.medscape.com/article/284667-overview",
#         "https://emedicine.medscape.com/article/284801-overview",
#         "https://emedicine.medscape.com/article/284983-overview",
#         "https://emedicine.medscape.com/article/285191-overview"]


#get_all_info("https://emedicine.medscape.com/article/170066-overview")