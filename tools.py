import json



def load_json(json_file_path):
    with open(json_file_path) as data_file:
        data = json.load(data_file)
    data_file.close()
    return data


def login(driver, log_info):
    username = driver.find_element_by_name('username')
    pw = driver.find_element_by_name('password')
    username.send_keys(log_info['username'])
    pw.send_keys(log_info['password'])

    # Log in button
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click()


# for col in [1, 2, 3]:
#     col = str(col)
#     image_i_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[' + row + ']/div[' + col + ']/a'
#     image_i = driver.find_element_by_xpath(image_i_xpath)
#     ActionChains(driver).move_to_element(image_i).perform()
#     image_i.click()
#
#     username_xpath = '/html/body/div[3]/div/div/div[2]/div/article/header/div[2]/div[1]/div/a'
#     username = driver.find_element_by_xpath(username_xpath).get_attribute('title')
#     if 'shop' in username:  # TODO A RETRAVAILLER
#         pass
#     else:
#         caption_xpath = '/html/body/div[3]/div/div/div[2]/div/article/div[2]/div[1]/ul/li'
#         caption = driver.find_element_by_xpath(caption_xpath).text
#
#         # Get hashtags with regex
#         hashtags_ = re.findall(r"#(\w+)", caption)
#         hashtags_ = list(set(hashtags_))
#         any_in = lambda a, b: bool(set(a).intersection(b))  # intersection between 2 lists
#         if any_in(forbidden, hashtags_):
#             pass
#         else:
#             hashtags_dict_analysis['searched_hashtags'][hashtag][hashtag_count] = hashtags_ #TODO CHANGE NAME
#             # Follow, like
#             try:
#                 if driver.find_element_by_xpath("//button[contains(.,'Following')]"):
#                     print(username + 'is already followed')
#             except NoSuchElementException :
#                 driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()
#                 time.sleep(random.uniform(0.2, 1))
#                 try:
#                     driver.find_element_by_xpath("//span[contains(.,'Like')]").click()
#                     like_count += 1
#                     hashtag_count += 1
#                 except NoSuchElementException:  # if already liked [contains(., 'Unlike)]
#                     pass
#             finally:
#                 time.sleep(random.uniform(0.2, 1))
#                 driver.find_element_by_xpath("//button[contains(.,'Close')]").click()
#                 driver.implicitly_wait(5)