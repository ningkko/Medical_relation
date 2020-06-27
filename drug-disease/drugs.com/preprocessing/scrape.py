#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import numpy as np 
import re
import csv


url = "https://www.drugs.com/medical_conditions.html"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')


condition_category_urls_raw = soup.find("ul", class_= "ddc-paging")


soup = BeautifulSoup(str(condition_category_urls_raw), 'html.parser')
all_a = soup.select('a')
condition_category_urls = []
for a in all_a:
    condition_category_urls.append('https://www.drugs.com'+str(a['href']))


def get_single_condition_url(_condition_urls, category_url ):
    req = requests.get(category_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    condition_urls_raw = soup.find("ul", class_= "ddc-list-column-2")
    soup = BeautifulSoup(str(condition_urls_raw), 'html.parser')
    all_a = soup.select('a')
    for a in all_a:
        _condition_urls.append('https://www.drugs.com'+str(a['href']))


condition_urls = []
for url in condition_category_urls:
    get_single_condition_url(condition_urls, url)


# function to get unique values 
def _unique(lst): 
    x = np.array(lst) 
    return np.unique(x)


condition_urls = _unique(condition_urls)
print(len(condition_urls))
condition_urls.sort()


condition_urls_1 = condition_urls[:2037]
condition_urls_2 = condition_urls[2037:]

def extract_string(section):
    '''
    returns a list of names
    '''
    pattern = r"</b>\n\s*(.*?)\s*</p>"
    synoms = re.findall(pattern, str(section), flags=0)
    return synoms


def get_condition_name_from_url_1(url):
    '''
    returns the name of a condition from a url
    '''
    pattern = r"condition/(.*?)\s*.html"
    name = re.findall(pattern, url, flags=0)
    name = name[0]
    name = name.replace("-", " ")
    return name 


def get_condition_name_from_url_2(url):
    '''
    returns the name of a condition from a url
    '''
    pattern = r".com/(.*?)\s*.html"
    name = re.findall(pattern, url, flags=0)
    name = name[0]
    name = name.replace("-", " ")
    return name 


def _clean_text(lst):
    # get rid of parentheses 
    lst = re.sub(r'\([^)]*\)', '', lst[0])
    # get rid of <>
    lst = re.sub(r'<.*?>', '', lst).split(",")
    # get rid of white spaces
    for i in range(len(lst)):
        lst[i] = lst[i].rstrip().lstrip()
    return lst
        
def get_subtitles(section):
    '''
    returns the list of generic names of a condition from a url
    '''
    generic_pattern = r'Generic Name:(.*?)(?=<b>|</p>)'
    generic_names = re.findall(generic_pattern, str(section), flags=0)
    if generic_names:
        generic_names = _clean_text(generic_names)
    
    brand_pattern = r'Brand Name:(.*?)(?=<b>|</p>)'
    brand_names = re.findall(brand_pattern, str(section), flags=0)
    if brand_names:
        brand_names = _clean_text(brand_names)

    return [generic_names, brand_names]


def get_rx_otc(section):
    pattern = r">(.*?)</span>"
    result =  re.findall(pattern, str(section), flags=0)
    return result[0]


def get_drug_class(section):
    pattern = r"drug-class/(.*?).html"
    return re.findall(pattern, str(section), flags=0)

def get_pregnancy_CSA(section):
    pattern = r">\n*\s*(.*?)\s*\n*</span>"
    return re.findall(pattern, str(section), flags=0)


def get_href(section):
    pattern = r"href=\"(.*?)\""
    result = re.findall(pattern, str(section), flags=0)
    
    return "https://www.drugs.com"+result[0]


def is_rx(section):
    '''
    returns true or false
    '''
    pattern = r"<span aria-hidden=\"true\">(.*?)\s*</span>"
    return re.findall(pattern, str(section), flags=0)[0] == 'Rx' 

def get_all_brands(section):
    pattern = r">(.*?)</span>"
    text = re.findall(pattern, str(section), flags=0)
    text = text[0].split(", ")
    return text


def get_drugs_for_condition(condition_url, url_type=1):
    disease_info = []
    
    condition_name = ""
    if url_type == 1:
        condition_name = get_condition_name_from_url_1(condition_url)
    else:
        condition_name = get_condition_name_from_url_2(condition_url)


    req = requests.get(condition_url)
    condition_soup = BeautifulSoup(req.content, 'html.parser')

    # get other names of the condition:
    other_name_raw = condition_soup.find("section", class_= "condition-table__synonyms condition-table__sub-section")
    synoms = extract_string(other_name_raw)
        
    disease_info = [[condition_name], [synoms]]

    # Each medication has three <tr> tags
    ### <tr class="condition-table__summary ddc-toggle-active">
    ### <tr class="condition-profile">
    ### <tr class="condition-table__responsive-spacer">
    # Medication name and Rx information are stored in "condition-table__summary ddc-toggle-active"
    # Generic names are stored in condition-profile

    drug_info = []
    
    drug_names = []
    rxs = []
    subtitles = []
    drug_classes = []
    pregnancy = []
    csa = []
    # Find condit/ion-table__summary for all medications under a condition
    body = condition_soup.findAll("tbody")
    if body:
        body = body[0]
        
        drug_name_section = body.findChildren("a", class_="condition-table__drug-name__link", recursive=True) # recursive == True: recursively find children of children 
        if drug_name_section: 
            for n in drug_name_section:
                drug_names.append(n.renderContents().decode("utf-8"))
                # get the link, go to page
                drug_link = get_href(n)
                req = requests.get(drug_link)
                drug_soup = BeautifulSoup(req.content, 'html.parser')
                
                drug_subtitle_section = drug_soup.findAll('p', class_="drug-subtitle")
                drug_subtitles = get_subtitles(drug_subtitle_section)
                
                all_brands_section = drug_soup.findAll('span', id="all_brands")
                if all_brands_section:
                    if drug_subtitles[1]:
                        # get rid of the ... show tag
                        full_brands = []
                        for i in range(len(drug_subtitles[1])):
                            if "..." not in drug_subtitles[1][i]:
                                full_brands.append(drug_subtitles[1][i])
                        # add remaining brands
                        remaining_brands = get_all_brands(all_brands_section)
                        full_brands += remaining_brands
                        # replace 
                        drug_subtitles[1] = full_brands
                    
                if drug_subtitles:
                    subtitles.append(drug_subtitles)
                else:
                    subtitles.append([])
                

                more_resource =  drug_soup.findAll('ul', class_="more-resources-list more-resources-list-general")
                if more_resource:
                    drug_classes.append(get_drug_class(str(more_resource)))
                else:
                    drug_classes.append([])

            # rx
            is_rx_section = body.findChildren("td", class_="condition-table__rx-otc", recursive=True)
            for r in is_rx_section:
                rxs.append(get_rx_otc(r))
            
#             # generic names
#             generic_name_section = body.findChildren("p", class_="condition-table__generic-name", recursive=True)
#             for gn in generic_name_section:
#                 drug_generic_names.append(get_generic_name(gn))
#             
#             # drug classes 
#             drug_class_section = body.findChildren("p", class_="condition-table__drug-classes", recursive=True)     
#             for dc in drug_class_section:
#                 drug_classes.append(get_drug_class(dc))

# generic names and drug classes cannot be extracted from the disease page since sometimes they are missing.
            
            # pregnancy class
            pregnancy_section = body.findChildren("td", class_="condition-table__pregnancy", recursive=True)     
            for ps in pregnancy_section:
                ps = get_pregnancy_CSA(ps)
                if ps:
                    pregnancy.append(ps[0])
                else: 
                    pregnancy.append([])
            
            # CSA class
            CSA_section = body.findChildren("td", class_="condition-table__csa", recursive=True)     
            for c in CSA_section:
                c = get_pregnancy_CSA(c)
                if c:
                    csa.append(c[0])
                else:
                    csa.append([])
                    
            #print(len(rxs), len(drug_names), len(subtitles), len(drug_classes), len(pregnancy), len(csa))
            for i in range(len(drug_names)):
                generic_names = []
                drug_brand = []
                
                # take care of empty lists
                if subtitles[i]:
                    generic_names = subtitles[i][0]
                    drug_brand = subtitles[i][1]
                
                drug_info.append([rxs[i], drug_names[i], generic_names, drug_classes[i], drug_brand, pregnancy[i], csa[i]])

    disease_info.append(drug_info)
    return disease_info


output_lst = []
i = 0
for url in condition_urls_1:
    #print(i/len(condition_urls_1))
    print(url)
    output_lst.append(get_drugs_for_condition(url))
    i += 1

for url in condition_urls_2:
    output_lst.append(get_drugs_for_condition(url, 2))


output_lst_copy = output_lst


for i in range(len(output_lst_copy)-1):
    if len(output_lst_copy[i][2])!= 0:
        print(len(output_lst_copy[i][2]))
        output_lst_copy[i][0] = output_lst_copy[i][0]*len(output_lst_copy[i][2])
        output_lst_copy[i][1] = output_lst_copy[i][1]*len(output_lst_copy[i][2])
    

with open("outut/output_full.csv", 'w') as file:
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

file.close()






