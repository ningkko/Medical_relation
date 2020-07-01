from utils import *

url = "https://emedicine.medscape.com"

surgery_fields = get_field(url,"div","browse-surgery")
surgery_field_urls = get_field_url(surgery_fields, url)

#-------- surgery subfields
i=0
surgery_article_links = []
for surgery_field_url in surgery_field_urls:
    print(i)
    article_name_page = get_field(surgery_field_url,"div","topic-section-wrap")
    surgery_article_link = get_field_url(article_name_page, url)
    print(surgery_article_link)
    name = "surgery_links/"+surgery_field_url.split(".com/")[1]+".txt"
    surgery_article_link = "\n".join(surgery_article_link)
    with open(name, "w") as text_file:
        text_file.write(surgery_article_link)
    i+=1
