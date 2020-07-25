# Author: Ning Hua        
# yhua@smith.edu

#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import numpy as np 
import re
import csv


def get_single_condition_url(_condition_urls, category_url ):
    req = requests.get(category_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    condition_urls_raw = soup.find("ul", class_= "ddc-list-column-2")
    soup = BeautifulSoup(str(condition_urls_raw), 'html.parser')
    all_a = soup.select('a')
    for a in all_a:
        _condition_urls.append('https://www.drugs.com'+str(a['href']))


# function to get unique values 
def unique(lst): 
    x = np.array(lst) 
    return np.unique(x)


def extract_string(section):
    '''
    returns a list of names
    '''
    pattern = r"</b>\n\s*(.*?)\s*</p>"
    synoms = re.findall(pattern, str(section), flags=0)
    return synoms


def get_condition_name_from_url(url):
    '''
    returns the name of a condition from a url
    '''
    pattern = r"condition/(.*?)\s*.html"
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


def get_hidden_drug_pages(condition_soup):
    hidden_page_urls = []
    nav = condition_soup.findAll("ul", class_="ddc-paging ddc-paging-result ddc-paging-condition-list")
 
    if nav:
        # only one nav tag in each page
        nav = nav[0]
        # find all unique urls in a nav tag
        urls = nav.findChildren("a", recursive=True) # recursive == True: recursively find children of children 
        if urls:
            for url_text in urls:
                # get the link, go to page
                hidden_page_urls.append(get_href(url_text))
    
    # print(hidden_page_urls)
    return hidden_page_urls


def get_drug_info_from_body(url):
    req = requests.get(url)
    condition_soup = BeautifulSoup(req.content, 'html.parser')

    body = condition_soup.findAll("table", class_="condition-table data-list data-list--nostripe ddc-table-sortable")   
    # get drugs on the page 
    drug_info = []

    if body:
        body = body[0]

        drug_names = []
        rxs = []
        subtitles = []
        drug_classes = []
        pregnancy = []
        csa = []

        drug_name_section = body.findChildren("a", class_="condition-table__drug-name__link", recursive=True) # recursive == True: recursively find children of children 
        # check if the disease page has more than one page of drug names
        if drug_name_section: 
            for n in drug_name_section:
                drug_names.append(str(n.renderContents().decode("utf-8")))
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
            
                # # generic names
                # generic_name_section = body.findChildren("p", class_="condition-table__generic-name", recursive=True)
                # for gn in generic_name_section:
                #     drug_generic_names.append(get_generic_name(gn))

                # # drug classes 
                # drug_class_section = body.findChildren("p", class_="condition-table__drug-classes", recursive=True)     
                # for dc in drug_class_section:
                #     drug_classes.append(get_drug_class(dc))

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
    return drug_info

def get_drugs_for_condition(condition_url):
    disease_info = []
    
    condition_name = ""
    condition_name = get_condition_name_from_url(condition_url)

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

    page_urls = [condition_url] + get_hidden_drug_pages(condition_soup)
    page_urls = unique(page_urls)
    print(len(page_urls))

    # print(page_urls)
    drug_info = []
    for url in page_urls:
        cur_drug_info = get_drug_info_from_body(url)
        drug_info += cur_drug_info


    disease_info.append(drug_info)
    # if len(page_urls)>1:
    print(condition_name)
    print(drug_info)

    return disease_info







