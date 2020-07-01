from utils import *

url = "https://emedicine.medscape.com"

pediatrics_fields = get_field(url,"div","browse-pediatrics")
pediatrics_field_urls = get_field_url(pediatrics_fields, url)

#-------- pediatrics subfields
i=0
pediatrics_article_links = []
for pediatrics_field_url in pediatrics_field_urls:
    print(i)
    article_name_page = get_field(pediatrics_field_url,"div","topic-section-wrap")
    pediatrics_article_link = get_field_url(article_name_page, url)
    print(pediatrics_article_link)
    name = "pediatrics_links/"+pediatrics_field_url.split(".com/")[1]+".txt"
    pediatrics_article_link = "\n".join(pediatrics_article_link)
    with open(name, "w") as text_file:
        text_file.write(pediatrics_article_link)
    i+=1
