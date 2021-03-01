import urllib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import time
from datetime import date



def job_search(job_title,position,driver):

    getVars = {'k': job_title, 'l': position}
   
    url = ('https://www.naukri.com/'+job_title+'-jobs-in-'+position+'?'+urllib.parse.urlencode(getVars))


    site = driver.get(url)

    page_source = driver.page_source

    time.sleep(10)
    soup = BeautifulSoup(page_source,"html.parser")
    driver.close()

    data = soup.find(class_='list')
    data_ele = soup.find_all("article",class_="jobTuple bgWhite br4 mb-8")

    job_title1 = []     #list for job title

    company = []        #list for company 

    links = []          #list for job links

    date_list = []      #list for job posted date

    for i in data_ele:

        job_t = i.find('a',class_="title fw500 ellipsis")
        job_title1.append(job_t.text)

        com = i.find('a',class_="subTitle ellipsis fleft")
        company.append(com.text)

        link = i.find('a',class_="title fw500 ellipsis")
        links.append(link.get("href"))

        date_l = i.find('span',class_="fleft fw500")
        date_list.append(date_l.text)

    #df = df.append({'Title':job_title1,'Company':company,'Job_Links':links,'Posted_Date':date_list})
    data = {'Job_Title':job_title1,'Company':company,'Job_Links':links,'Posted_Date':date_list}

    df = pd.DataFrame(data)
    # print(df)

    return df


def create_folder():

    file_path = os.path.abspath(__file__)
    # print(file_path)

    parent_dir = os.path.dirname(file_path)
    # print(parent_dir)

    today = date.today()
    today_format = today.strftime('%d-')+today.strftime('%b-')+today.strftime('%Y')
    
    folder_name = str(today_format)
    # print(folder_name)

    path = os.path.join(parent_dir,folder_name)
    print(path)

    isdir = os.path.isdir(path)
    print(isdir)

    k = 1

    while(isdir):
        print(isdir)

        temp = path
        temp = temp+str("_"+str(k))
        k = k+1
        isdir = os.path.isdir(temp)
        print(isdir)
        if isdir==False:
            path = temp

    print(path)
    os.mkdir(path)
    print(path)
    # print(path)
    return path

def create_excel(df,path):

    excel_filename = path+"/Naukari_Dot_Com.xlsx"
    print(excel_filename)
    df.to_excel(excel_filename, index=False)

if __name__== "__main__":

    job_title = input("Job Title >")
    location = input("Location >")
    location_of_driver = "/usr/bin"
    driver = webdriver.Chrome(executable_path=(location_of_driver + "/chromedriver"))

    data = job_search(job_title,location,driver)        #function for scraping website

    path = create_folder()                              #function for creating folder
    
    create_excel(data,path)                             #function excel for storing data
