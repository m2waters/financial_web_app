from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
import csv, json, time
import logging, os
from dataclasses import dataclass, field, fields, asdict
from concurrent.futures import ThreadPoolExecutor


def get_post(url, retries=3):
    tries = 0
    success = False

    while tries <= retries and not success:
        driver = webdriver.Firefox()
        try:
            driver.get(url)
            time.sleep(1)
            raw_data = driver.find_element(By.ID, "rawdata-tab")
            raw_data.click()
            time.sleep(1)
            json_text = driver.find_element(By.TAG_NAME, "pre").text
            print(json_text)
            resp = json.loads(json_text)
            print(resp)
            if resp:
                success = True
                children=resp["data"]["children"]
                for child in children:
                    data = child["data"]
                    name = data["title"]
                    author = data["author_fullname"]
                    permalink = data["permalink"]
                    upvote_ratio = data["upvote_ratio"]

                    print("Name : ", name)
                    print("Author : ", author)
                    print("Permalink : ", permalink)
                    print("Upvotes : ", upvote_ratio)

        except Exception as e:
            tries += 1
            print("error in pulling data")
    
        finally:
            driver.quit()

    with open("extracted_text/json_data.json", 'w') as file:
        json.dump(resp, file)


get_post(url="https://www.reddit.com/r/investing.json")