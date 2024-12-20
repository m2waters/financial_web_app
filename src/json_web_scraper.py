from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
import csv, json, time
from dataclasses import dataclass, field, fields, asdict
import sqlite3


def open_db_connection(database='database.db'):
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    return (cur, connection)

@dataclass
class TempDataStore:

    post_title: str = ""
    author: str = ""
    permalink: str = ""
    subreddit: str = ""
    upvote_ratio: float = 0.0

    def __post_init__(self):
        self.validate_string()

    def validate_string(self):

        for field in fields(self):

            if isinstance(getattr(self, field.name), str):

                if getattr(self, field.name) == '':
                    setattr(self, field.name, "NULL")
                    continue
                
                field_value = getattr(self, field.name)
                setattr(self, field.name, field_value.strip())


class StoreData:

    def __init__(self, storage_queue_limit=100):
        self.permalinks_seen = []
        self.storage_queue = []
        self.storage_queue_limit = storage_queue_limit
        self.db_connection_open = False


    def save_to_db(self):
        
        data_to_save = []
        data_to_save.extend(self.storage_queue)
        self.storage_queue.clear()
        if not data_to_save:
            return
        for data_point in data_to_save:
            
            cursor, connection = open_db_connection()
            self.db_connection_open = True
            cursor.execute(
                "INSERT INTO reddit_posts (post_title, author, permalink, subreddit, upvote_ratio) VALUES (?, ?, ?, ?, ?)",
                (data_point.post_title,
                data_point.author,
                data_point.permalink,
                data_point.subreddit,
                data_point.upvote_ratio
                )
            )
            connection.commit()
            connection.close()
            self.db_connection_open = False
    def is_duplicate(self, input_data):
        if input_data.permalink in self.permalinks_seen:
            return True
        self.permalinks_seen.append(input_data.permalink)
        return False
    
    def add_data(self, scraped_post):
        if self.is_duplicate(scraped_post) == False:
            self.storage_queue.append(scraped_post)
            if len(self.storage_queue) >= self.storage_queue_limit and self.db_connection_open == False:
                self.save_to_db()

def get_post(url, retries=3, data_pipeline=None):
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
            
            resp = json.loads(json_text)
            
            if resp:
                success = True
                children=resp["data"]["children"]
                for child in children:
                    data = child["data"]

                    post = TempDataStore(
                        post_title = data["title"],
                        author = data["author_fullname"],
                        permalink = data["permalink"],
                        subreddit = data["subreddit_name_prefixed"],
                        upvote_ratio = data["upvote_ratio"]
                    )
      
                    data_pipeline.add_data(post)

        # except Exception as e:
        #     tries += 1
        #     print("error in pulling data")
    
        finally:
            driver.quit()

    with open("extracted_text/json_data.json", 'w') as file:
        json.dump(resp, file)



start_time = time.time()
limit = 100
feed_pipeline = StoreData(storage_queue_limit=100)
get_post(url="https://www.reddit.com/r/investing.json?limit={}".format(limit), data_pipeline=feed_pipeline)
feed_pipeline.save_to_db()

end_time = time.time()
time_taken = round(end_time - start_time, 2)
print(f'Time to run for {limit} posts: {time_taken} seconds')
