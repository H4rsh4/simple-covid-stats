import requests
from bs4 import BeautifulSoup


def get_covid_update():
    url = "https://www.worldometers.info/coronavirus/"
    #driver = webdriver.Firefox()
    page = requests.get(url)
    page_source = page.text

    #driver.get("https://www.worldometers.info/coronavirus/")

    Total = 0
    #content = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    Cases = {
        'Total Number of Cases': 0,
        'Total Number of Deaths': 0,
        'And Total Number of Recovered Cases': 0,
    }
    emp = [] + list(Cases.keys())
    num = 0
    for place in soup.find_all('div', class_='maincounter-number'):
        Cases[emp[num]]=str(place.span.string).strip(' ')
        num+=1
    return Cases