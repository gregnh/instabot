
# coding: utf-8

# In[1]:

# import pandas as pd
# import numpy as np
import random
import sys, time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException #, ElementNotVisibleException

sys.path.append('../')

def load_json(json_file_path):
    with open(json_file_path) as data_file:
        data = json.load(data_file)
    data_file.close()
    return data


# In[41]:

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(5)

url='https://www.instagram.com/?hl=en'
driver.get(url)


# In[42]:

# Access to log in page
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
driver.implicitly_wait(5)


# In[43]:

# Log in task
mail= driver.find_element_by_name('username')
pw = driver.find_element_by_name('password')
log = load_json('../instaboost/info.json')
mail.send_keys(log['username'])
pw.send_keys(log['password'])
# Log in button
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click()
driver.implicitly_wait(5)


# In[44]:

like_count = 0
# Search bar

# TODO for loop pour pick le hashtag randomly
hashtag = log['search'][0]

new_followed = {#'date': time.strftime('%d/%m/20%y_%H:%M:%S', time.localtime()),
                 'searched_hashtags': {hashtag: {}
                                      },
                }

# Forbidden #
forbidden = load_json('../instaboost/forbidden_hashtags.json')
forbidden = [str(i) for i in forbidden['hashtags']]


# In[45]:

search = driver.find_element_by_css_selector('input[placeholder="Search"]') # find Searh bar
search.send_keys(hashtag)

# Click on first link
driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').click()


# In[46]:

# # Click on 'Load More'
try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_link_text('Load more').click()
except NoSuchElementException:
    pass

# Click on first photo
first_photo_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]/a'
first_photo = driver.find_element_by_xpath(first_photo_xpath)
ActionChains(driver).move_to_element(first_photo).perform() # remonter vers la 1er image de 'Most recent'


# In[47]:

first_photo.location


# Lines structure
# 
# Premiere ligne  
# //*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]/a #1st photo
# 
# //*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[2]/a #2nd photo
# 
# Seconde ligne  
# //*[@id="react-root"]/section/main/article/div[2]/div[1]/div[2]/div[1]/a

# In[48]:

# count_row_scroll = 0
# # try:
# row = 1
# while True:
# #     row = str(row) 
#     count_row_scroll += 1


# In[53]:

row = str(1)  # REMOVE
hashtag_count = 1
for col in [1,2,3]:
    col = str(col)
    image_i_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div['+row+']/div['+col+']/a'
    image_i = driver.find_element_by_xpath(image_i_xpath)
    ActionChains(driver).move_to_element(image_i).perform()
    image_i.click()

    username_xpath = '/html/body/div[3]/div/div/div[2]/div/article/header/div[2]/div[1]/div/a'
    username = driver.find_element_by_xpath(username_xpath).get_attribute('title')
    if 'shop' in username: #TODO A RETRAVAILLER
        pass
    else:
        caption_xpath = '/html/body/div[3]/div/div/div[2]/div/article/div[2]/div[1]/ul/li'
        caption = driver.find_element_by_xpath(caption_xpath).text

        # Get hashtags with regex
        hashtags_ = re.findall(r"#(\w+)", caption)
        hashtags_ = list(set(hashtags_))
        any_in = lambda a, b: bool(set(a).intersection(b)) # intersection between 2 lists
        if any_in(forbidden, hashtags_):
            pass
        else:
            new_followed['searched_hashtags'][hashtag][hashtag_count] = hashtags_
            # Follow, like
            try:
                if driver.find_element_by_xpath("//button[contains(.,'Following')]"):
                    print(username + 'is already followed')
            except(NoSuchElementException):
                driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()
                time.sleep(random.uniform(0.2,1))
                try:
                    driver.find_element_by_xpath("//span[contains(.,'Like')]").click()
                    like_count += 1
                    hashtag_count += 1
                except NoSuchElementException: # if already liked [contains(., 'Unlike)]
                    pass
            finally:
                time.sleep(random.uniform(0.2,1))
                driver.find_element_by_xpath("//button[contains(.,'Close')]").click()
                driver.implicitly_wait(5)


# In[ ]:

# Scroll down
if count_row_scroll == 4: # 1 new load = 4 lignes de charger
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(0.3,0.8))
    count_row_scroll = 0

row += 1

#         if like_count == random.randint(25,45): # tous les 35 likes, stop
#             # time.sleep(60*random.uniform(20,45))
#             # print('Onto the next : %s' %(time.strftime('%d/%m/20%y_%H:%M:%S', time.localtime())))
        
# except(NoSuchElementException): # if no more image
#     scroll = False
#     pass # look for another hashtag in search bar


# In[53]:

new_following['searched_hashtags'].clear()
new_following


# In[32]:

driver.quit()


# Doc :
# - Regex hastag :  
# https://stackoverflow.com/questions/38506598/regular-expression-to-match-hashtag-but-not-hashtag-with-semicolon  
# https://stackoverflow.com/questions/2527892/parsing-a-tweet-to-extract-hashtags-into-an-array-in-python
# 
# 
# - Run script when booting, automatically :  
# linux reboot  and lauch a program with terminal  
# https://unix.stackexchange.com/questions/19634/what-is-the-linux-equivalent-of-windows-startup  
# https://stackoverflow.com/questions/7221757/run-automatically-program-on-startup-under-linux-ubuntu  
# https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu
# 

# In[5]:

import platform
platform.architecture()


# In[22]:

import time
time.localtime()


# In[ ]:



