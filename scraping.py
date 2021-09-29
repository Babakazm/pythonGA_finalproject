from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import selenium
import selenium.webdriver
import time

url='https://www.imdb.com/chart/boxoffice/'

driver = selenium.webdriver.Chrome()
driver.get(url)
time.sleep(1)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings = soup.find_all('h1')
heading=[]
time.sleep(1)
for subhead in subheadings:
    print(subhead.text)
    t=str(subhead.get_text())
    heading.append(t)

time.sleep(1)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings5 = soup.find_all('h4')
time_of_play=[]
time.sleep(1)
for subhead5 in subheadings5:
    print(subhead5.text)
    o=str(subhead5.get_text())
    heading.append(o)

print(time_of_play)

time.sleep(1)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings1 = soup.find_all('th')
title=[]
time.sleep(1)
for subhead1 in subheadings1:
    print(subhead1.text)
    s=str(subhead1.get_text())
    title.append(s)
print(title)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings2 = soup.find_all('td',class_='titleColumn')
movie=[]
time.sleep(1)
for subhead2 in subheadings2:
    print(subhead2.text)
    m=str(subhead2.get_text())
    movie.append(m)
print(movie)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings3 = soup.find_all('td',class_='ratingColumn')
weekend=[]
time.sleep(1)
for subhead3 in subheadings3:
    print(subhead3.text)
    w=str(subhead3.get_text())
    weekend.append(w)
print(weekend)
source = driver.page_source
soup = BeautifulSoup(source)
subheadings4 = soup.find_all('span',class_='secondaryInfo')
gross=[]
time.sleep(1)
for subhead4 in subheadings4:
    print(subhead4.text)
    g=str(subhead4.get_text())
    weekend.append(g)
print(gross)

for i in range(len(movie)):
    print (f"{heading} for {time_of_play} is {i}:{movie[i]} and sold {weekend[i]}")