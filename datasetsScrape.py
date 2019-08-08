# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 20:09:02 2019

@author: Srikanth
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import requests 
import re


def csv_downloader(file_url,name):     
    file_name = re.sub('[^a-zA-Z0-9" "\. ]'," ",name) 
    print( "Downloading file:%s\n"%file_name )  
    r = requests.get(file_url, stream = True) 
    
    with open(file_name,"wb") as csv: 
        for chunk in r.iter_content(chunk_size=1024): 
             if chunk: 
                 csv.write(chunk)
    print("%s downloaded!\n"%file_name)            


myurl = "https://www.datacamp.com/tracks/data-scientist-with-python"
url_connection = urlopen(myurl)
page_html = url_connection.read()
page_soup = soup(page_html,"html.parser")
url_connection.close()

course_list = page_soup.find_all("li",{"track__course"})
course_list.pop()
    
course_links = []
for course in course_list:
    course_links.append("https://www.datacamp.com"+course.find('a')['href'])

data_links = [] 
data_set_names = []
    
for myurl in course_links[10:11]:
    url_connection = urlopen(myurl)
    page_html = url_connection.read()
    url_connection.close() 
    page_soup = soup(page_html,"html.parser")
    data = page_soup.find_all("li",{"course__dataset"})
    
for d in data:    
    data_links.append(d.find("a")['href'])
    data_set_names.append(d.find("a").text.strip())
    
for link,name in zip(data_links,data_set_names):
    name = name + link[-4:]
    csv_downloader(link,name)

    



    