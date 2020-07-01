from utils import *

url = "https://emedicine.medscape.com"

medicine_fields = get_field(url,"div","browse-medicine")
medicine_field_urls = get_field_url(medicine_fields, url)

#-------- medicine subfields
i=0
medicine_article_links = []
for medicine_field_url in medicine_field_urls:
    print(i)
    article_name_page = get_field(medicine_field_url,"div","topic-list alpha")
    medicine_article_link = get_field_url(article_name_page, url)
    print(medicine_article_link)
    name = "links/"+medicine_field_url.split(".com/")[1]+".txt"
    medicine_article_link = "\n".join(medicine_article_link)
    with open(name, "w") as text_file:
        text_file.write(medicine_article_link)
    i+=1