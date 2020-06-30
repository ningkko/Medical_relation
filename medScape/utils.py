from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from os import path

# --------- GENERAL UTILS ----------
def get_field(url, _container, _class):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    fields = soup.find(_container, class_=_class)
    # print(soup.prettify())
    return fields


def get_field_url(fields, mother_url):
    field_soup = BeautifulSoup(str(fields), 'html.parser')
    all_a = field_soup.select('a')
    # print(all_a)
    urls = []
    for a in all_a:
        a_url = str(a['href'])
        if "http" in a_url:
            urls.append(a_url)
        else:
            urls.append(mother_url + a_url)

    return urls



# ------------ MEDICINE UTILS -------------

def get_title_content(_url, _title_container, _content_container, _class):
    'returns a list of content'
    req = requests.get(_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    lst = []

    # look for the title only for one time
    if "overview" in _url:
        titles = soup.find_all(_title_container)
        if len(titles) > 1:
            # add the title
            lst.append(titles[0].text)
        if len(titles) == 0:
            print("No title: ")
            print(_url)

    content_box = soup.find(_content_container, id=_class)
    content = content_box.find_all("p")
    for c in content:
        lst.append(c.text)

    return lst
    # return fields


# get all information of a medical term
def get_next_section(_url):

    fields = get_field(_url, "div", "next_section_btn")
    field_soup = BeautifulSoup(str(fields), 'html.parser')
    field_url = field_soup.select('a')

    if field_url:
        next_section_url = field_url[0]['href']
        # print(next_section_url)

        if "http" in next_section_url:
            return next_section_url
        else:
            _id = next_section_url.split("-")[1] + "#showall"
            prefix = _url.split("-")[0]
            next_section_url = prefix + "-" + _id
            return next_section_url
    else: 
        return ""


# get -rticle page in a drug-disease topic
def get_all_info(_url, type):

    medical_term_info_full = []
    # first scrape -overview#showall since every page starts here.
    show_all_url = _url + "#showall"   # #showall wouldn't affect if there's no such action
    overview_info = get_title_content(show_all_url, "title", "div", "drugdbmain")
    # write to txt
    title = overview_info[0]
    title = re.sub(r"[,.;@#?!&$/<>()^*-_+={}\[\]\"\']+\ *", " ", title).strip().replace("  "," ")

    if type == "medicine":
        _path = 'medicine_txts/'+title+".txt"
    elif type == "surgery":
        _path = 'surgery_txts/'+title+".txt"
    elif type == "pediatrics":
        _path = 'pediatrics_txts/'+title+".txt"
    else:
        _path = 'unkown/'+title+".txt"
        
    # print(_path)
    # check if already in output
    is_existed = path.exists(_path)
    if is_existed:
        print("Aready downloaded. Skipped.")
        return

    # add to the retun list
    medical_term_info_full.append(overview_info)

    # check if next section
    next_section_url = get_next_section(show_all_url)

    while next_section_url and "questions-and-answers" not in next_section_url:
        print("Going to: " + next_section_url)
        info = get_title_content(show_all_url, "title", "div", "drugdbmain")
        medical_term_info_full.append(info)
        next_section_url = get_next_section(next_section_url)

    for i in range(len(medical_term_info_full)):
        medical_term_info_full[i] = "\n".join(medical_term_info_full[i])
        i += 1

    with open(_path, "w") as text_file:
        text_file.write("\n".join(medical_term_info_full))

    print("Finished.")
    return
