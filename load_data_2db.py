
import subprocess
import os
import sys
import shutil
import glob
import mysql.connector
from random import randint


filepath = '/Users/neneko/Documents/GitHub/UMLS-Mapping/nlp/'
source_folders = ['MayoClinic/', 'medlineplus/', 'MSDManual/',  'wikipedia/', 'uptodate/', 'medscape/']

mydb = mysql.connector.connect(host = "localhost",user = "root",password = "")

mycursor = mydb.cursor()

mycursor.execute("USE selah_umls")

for folder in source_folders:
    table_name = folder.replace("/","")
    mycursor.execute("CREATE TABLE "+table_name+" (article_id INT, random_num_1 INT, random_num_2 INT, Article_Title TEXT, Article_Text LONGTEXT)")
    files = os.listdir(filepath+folder)
    files.sort()
    table_name = folder.replace("/","")
    id = 0
    for file in files:
        content = ""
        with open(filepath+folder+file, "r") as f:
            content = f.read()
        sql = "INSERT INTO " + table_name + "(article_id, random_num_1, random_num_2, Article_Title, Article_Text) VALUES (%s, %s, %s, %s, %s)"
        val = (id, randint(0,99999), randint(0,99999),file, content)
        mycursor.execute(sql, val)

        mydb.commit()

        id += 1
