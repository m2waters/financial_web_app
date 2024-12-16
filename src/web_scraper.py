import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def open_more_replies(tag_name="button"):
    
    driver_buttons = driver.find_elements(By.TAG_NAME, tag_name)
    time.sleep(5)
    for button in driver_buttons:
        if "more replies" in button.text or "more reply" in button.text: # or "more comments" in button.text:
            button.click()
    time.sleep(5)
    
def view_more_comments():
    driver_buttons = driver.find_elements(By.TAG_NAME, "button")

    for button in driver_buttons:
        if "more comments" in button.text:
            button.click()
    time.sleep(5)

def is_there_more_comments():
    driver_buttons = driver.find_elements(By.TAG_NAME, "button")
    continue_searching = False
    for button in driver_buttons:
        if "more comments" in button.text:
            continue_searching=True
            break
    time.sleep(5)
    return continue_searching
    
def pull_out_text(tag_name="p"):
    driver_elements = driver.find_elements(By.TAG_NAME, tag_name)
    return [element.text for element in driver_elements]

def print_out_text(elements):
    for element in elements:
        print(element)
        print("\n\n")

link = "https://www.reddit.com/r/investing/comments/1hevl5p/what_did_you_learn_from_the_2008_recession_and/"

r = requests.get(link)

soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('div', class_='entry_content')
content = soup.find_all('p')
post_links = soup.find_all('faceplate-screen-reader-content')
content_href = soup.find_all('shreddit-post')



# print(content)

driver = webdriver.Firefox()
driver.get(link)
driver.implicitly_wait(100)
open_more_replies()
comments = is_there_more_comments()
while comments == True:

    view_more_comments()
    open_more_replies()
    
    comments = is_there_more_comments()








# button_content = pull_out_text(tag_name="button")
paragraph_content = pull_out_text()


# content_text = driver_content.text
driver.quit()

print_out_text(paragraph_content)
print(len(paragraph_content))