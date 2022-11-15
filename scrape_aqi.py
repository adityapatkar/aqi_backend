from bs4 import BeautifulSoup
import requests
import re

def scrape_real_time_aqi(city):
    link = f"https://www.aqi.in/dashboard/india/maharashtra/{city}"
    page_text = requests.get(link).text
    soup = BeautifulSoup(page_text)
    pattern = re.compile('The real-time air quality in Pune is [0-9]+')
    div =  soup.find_all("div", attrs={"class": "panel-body px-1 mb-4"})
    for div_single in div:
        p = div_single.find_all("p")
        for para in p:
            if(pattern.match(str(para.string))):
            #print(pattern.search(str(para.string)).group())
                num = re.compile("[0-9]+").search(pattern.search(str(para.string)).group())
                return float(num.group())
    return -1
