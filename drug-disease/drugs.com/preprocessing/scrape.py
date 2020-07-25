# Author: Ning Hua        
# yhua@smith.edu

#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import numpy as np 
import re
import csv
from utils import *
from datetime import datetime


with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/drugs.com/preprocessing/output/log.txt","a") as log:


    url = "https://www.drugs.com/medical_conditions.html"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')


    condition_category_urls_raw = soup.find("ul", class_= "ddc-paging")


    soup = BeautifulSoup(str(condition_category_urls_raw), 'html.parser')
    all_a = soup.select('a')
    condition_category_urls = []
    for a in all_a:
        condition_category_urls.append('https://www.drugs.com'+str(a['href']))


    condition_urls = []
    for url in condition_category_urls:
        get_single_condition_url(condition_urls, url)


    condition_urls = unique(condition_urls)
    print(len(condition_urls))
    condition_urls.sort()

    # track time elapsed

    output_lst = []
    i = 0
    for url in condition_urls:
        if i%20==0:
            now = datetime.now()
            log.write("\n--------------------"+now.strftime("%H:%M:%S")+"----------------\n")
            
        log.write(url+"\n")
        #print(i/len(condition_urls_1))
        output_lst.append(get_drugs_for_condition(url))
        i += 1

    output_lst_copy = output_lst


for i in range(len(output_lst_copy)-1):
    if len(output_lst_copy[i][2])!= 0:
        # print(len(output_lst_copy[i][2]))
        output_lst_copy[i][0] = output_lst_copy[i][0]*len(output_lst_copy[i][2])
        output_lst_copy[i][1] = output_lst_copy[i][1]*len(output_lst_copy[i][2])
    

with open("/n/data1/hsph/biostat/celehs/yih798/drug-disease/drugs.com/preprocessing/output/output_full.csv", 'w') as file:
        pen = csv.writer(file)
        # header
        pen.writerow(["disease name", "other names", "RX/OTC", "drug", "generic name", "drug class", "brand names", "pregnancy label", "CSA label"])
        
        # every row is a medication
        for row in output_lst_copy:
            for i in range(len(row[0])):
                if row[2]:
                    pen.writerow([row[0][i],row[1][i],row[2][i][0],row[2][i][1],row[2][i][2],
                                  row[2][i][3],row[2][i][4],row[2][i][5],row[2][i][6]])
                else:
                    pen.writerow([row[0][i],row[1][i]])


