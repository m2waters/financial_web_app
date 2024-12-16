import requests
from bs4 import BeautifulSoup
from selenium import webdriver

link = "https://www.reddit.com/r/investing/comments/1hevl5p/what_did_you_learn_from_the_2008_recession_and/"

r = requests.get(link)

soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('div', class_='entry_content')
content = soup.find_all('p')
post_links = soup.find_all('faceplate-screen-reader-content')
content_href = soup.find_all('shreddit-post')



print(content)

driver = webdriver.Firefox()
driver.get(link)

driver.implicitly_wait(100)

driver.get("https://google.co.uk/search?q=football")

driver.implicitly_wait(100)

driver.quit()