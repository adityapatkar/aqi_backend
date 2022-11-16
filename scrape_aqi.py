from bs4 import BeautifulSoup
import requests
import re


def scrape_real_time_aqi(city, state):
    link = f"https://www.aqi.in/dashboard/india/{state}/{city}"
    page_text = requests.get(link).text
    soup = BeautifulSoup(page_text)
    pattern = re.compile(
        f'The real-time air quality in {city} is [0-9]+'.lower())
    div = soup.find_all("div", attrs={"class": "panel-body px-1 mb-4"})
    for div_single in div:
        p = div_single.find_all("p")
        for para in p:
            if (pattern.match(str(para.string.lower()))):
                #print(pattern.search(str(para.string)).group())
                num = re.compile("[0-9]+").search(
                    pattern.search(str(para.string.lower())).group())
                return float(num.group())
    return -1
