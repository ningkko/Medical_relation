from utils import *
import sys

import os
files = os.listdir("links/medicine_links")

i = 0
# each file
for file in files:
	with open("links/medicine_links/" + file) as fp:
		# each url
		url = fp.readline()
		while url:
			
			i+=1
			print(str(i/7887) + "+++++++++++++++++++")
			# Had the following error message:
			# # Aready downloaded. Skipped.
			# # 0.9538481044757195+++++++++++++++++++
			# # On: https://emedicine.medscape.com/article/2500114-overview

			# # Aready downloaded. Skipped.
			# # 0.9539748953974896+++++++++++++++++++
			# # On: https://emedicine.medscape.com/article/2500121-overview

			# # Traceback (most recent call last):
			# #   File "medical_txts.py", line 18, in <module>
			# #     get_all_info(url.strip(), type="medicine")
			# #   File "/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/utils.py", line 130, in get_all_info
			# #     with open(_path, "w") as text_file:
			# # OSError: [Errno 36] File name too long: '/n/data1/hsph/biostat/celehs/yih798/drug-disease/MedScape/medicine_txts/Coronavirus Disease 2019 COVID-19 Autopsy Guidance FAQ What Are the Appropriate Collection Procedures If an Autopsy Is Performed for a Suspected Coronavirus Disease 2019 COVID-19 Case What Are the Appropriate Collection Procedures If an Autopsy Is Not Performed for a Suspected Coronavirus Disease 2019 COVID-19 Case What Are the Appropriate Collection Procedures If an Autopsy Is Performed for a Confirmed Coronavirus Disease 2019 COVID-19 Case.txt'


			# Original url count: 7887
			# >>> import math
			# >>> start_from = int(math.floor(0.9538481044757195 * 7887))
			# >>> 
			# >>> start_from
			# 7523

			# So start from 7523 

			# if i >= 7523:
			print("On: " + url)
			get_all_info(url.strip(), type="medicine")

			url = fp.readline()

# test = ["https://emedicine.medscape.com/article/135478-overview",
#         "https://emedicine.medscape.com/article/285433-overview",
#         "https://emedicine.medscape.com/article/284667-overview",
#         "https://emedicine.medscape.com/article/284801-overview",
#         "https://emedicine.medscape.com/article/284983-overview",
#         "https://emedicine.medscape.com/article/285191-overview",
#         "https://emedicine.medscape.com/article/170066-overview"]

# for t in test:
# 	get_all_info(t, type="medicine")