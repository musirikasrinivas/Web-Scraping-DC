# -*- coding: utf-8 -*-
"""
Spyder Editor 

This is a temporary script file.
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os
import re
import requests


def video_downloader(downloadable_links,video_names):    
    i = 0
    n = 1
    video_index = int(downloadable_links[0].split("/")[-1][2]) * 100 + n                

    for link in downloadable_links:        
        if video_index < int(link.split("/")[-1][2])*100:
            n = 1
            video_index = int(link.split("/")[-1][2])*100+n
        file_name = str(video_index) + " - " + video_names[i]            
        video_index = video_index + 1      
        
        file_name = re.sub('[^a-zA-Z0-9" " ]'," ",file_name) + ".mp4"
        if not os.path.isfile(file_name):
            print( "Downloading file:%s\n"%file_name )
            r = requests.get(link, stream = True)
            with open(file_name, 'wb') as f: 
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk: 
                        f.write(chunk)      
            print("%s downloaded!\n"%file_name)
        else:
            print("%s already exists!\n"%file_name)
        i = i + 1
                    
        

def pdf_downloader(unique_pdf_list,chapter_names):
    pdf_index = 0
    for link,name in zip(unique_pdf_list,chapter_names):
        pdf_index = pdf_index + 100
        file_name = str(pdf_index) + " - " + re.sub('[^a-zA-Z0-9" " ]'," ", name) + ".pdf" 
        if not os.path.isfile(file_name):           
            print( "Downloading file:%s\n"%file_name )
            r = requests.get(link, stream = True)
            with open(file_name, 'wb') as f: 
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk: 
                        f.write(chunk)      
            print("%s downloaded!\n"%file_name)
        else:
            print("%s already exists!\n"%file_name)
        

downloadable_video_links = []

def basedon9(link):
    return link[-9:]     
    

def basedon12(link):
    return link[-12:]

def modifying_to_downloadable_link():
    actual_videos = list(set(video_dup))
    for l in actual_videos:
        downloadable_video_links.append("https://" + l.replace("transcoded","transcoded_mp4").replace("hls-","").replace(".master.m3u8",".mp4"))
    downloadable_video_links.sort(key=basedon9)
    
    
unique_pdf_list = []

def list_of_pdfs():
    unique_pdf = list(set(pdf_dup))
    for i in unique_pdf:
        unique_pdf_list.append("https://" + i)
    unique_pdf_list.sort(key=basedon12)
    




myurl = "https://www.datacamp.com/tracks/data-scientist-with-python"
url_connection = urlopen(myurl)
page_html = url_connection.read()
page_soup = soup(page_html,"html.parser")
url_connection.close()

#creating track directory

track_dir = page_soup.find("h1", {"header-hero__title"}).text.strip()

if not os.path.exists(track_dir):
    os.mkdir(track_dir)
os.chdir(track_dir)

#getting course names, course links and creating course directories   

course_list = page_soup.find_all("li",{"track__course"})
course_list.pop()
    
course_links = []
course_names = []
course_index = 101
video_names = []
for course in course_list:
    course_links.append("https://www.datacamp.com"+course.find('a')['href'])
    course_title =course.find("h4",{"course-block__title"}).text.strip().replace(":"," ")       
    course_dir = str(course_index) + " - " + course_title
    course_names.append(course_dir)
    if not os.path.exists(course_dir):
        os.mkdir(course_dir)    
    course_index = course_index + 1

course_num = int(input("Enter course num to be downloaded---ex:(101,102):"))
course_num = course_num - 101
course_range = range(course_num, course_num + 1)

download_course = []
for i in course_range:
    download_course.append(i)

myurl = course_links[course_num]
url_connection = urlopen(myurl)
page_html = url_connection.read()
url_connection.close() 
page_soup = soup(page_html,"html.parser")
chapter_list = page_soup.find_all("li",{"chapter"})
os.chdir(course_names[course_num])

chapter_names = []
for chapter in chapter_list:       
    chapter_names.append(chapter.find("h4",{"chapter__title"}).text.strip())

    
        
#getting exercise links and exercise names
        
exe_names = []
exe_links = []
exercise_list = page_soup.find_all("li", {"chapter__exercise"})        
for exe in exercise_list:
    exe_names.append(exe.find("h5",{"chapter__exercise-title"}).text.strip())
    exe_a_tag = exe.find("a",{"chapter__exercise-link"})
    exe_span = exe_a_tag.find("span",{"chapter__exercise-icon"})
    type_of_exe = exe_span.find('img')["alt"][14]
    
    if (type_of_exe == "v") :
        video_names.append(exe_names[-1])
        exe_links.append(exe.find("a")["href"])
print("...............................................")
#getting video and pdf links from exercise_link 

video_dup = []  
pdf_dup = []            
for myurl in exe_links:                
    url_connection = urlopen(myurl)
    page_html = url_connection.read()
    page_soup = soup(page_html,"html.parser")
    url_connection.close()
    script = page_soup.find_all("script")[0]                
    video_pattern = re.compile("videos.data[a-zA-Z.\/0-9_-]*m3u8") #regular expression generator for video links
    video_link = re.findall(video_pattern, script.text)
    pdf_pattern = re.compile("s3.amazon[a-zA-Z0-9.\/-_]*pdf")   #regular expression generator for pdf links
    pdf_link = re.findall(pdf_pattern, script.text)
    pdf_dup.extend(pdf_link)
    video_dup.extend(video_link)


list_of_pdfs()        
pdf_downloader(unique_pdf_list,chapter_names)
modifying_to_downloadable_link() 
video_downloader(downloadable_video_links,video_names)
os.chdir("..//..")

    
                   
             
    
        
        
    
    


