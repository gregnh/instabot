import random
import time
# import re
import tools
import fire
import os
# import platform
# import imp
import psutil

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException  # , ElementNotVisibleException


#TODO page error : xpath = /html/body/div/div[1]/div/div/h2
# css selector? = Sorry, this page isn't available

class Main(object):
	def __init__(self, max_like_per_round=random.randint(30,35), op_sys='linux'):
		self.max_like_per_round = max_like_per_round
		self.op_sys = op_sys
		self.start = time.localtime()

	def restart(self):
		if self.op_sys == 'linux':
			os.system("shutdown /r /t 1")
		else:
			os.system("shutdown -r -t 1")

	def run(self):
		like_count = 0
		# hashtags_dict_analysis = {'searched_hashtags': {}} #TODO

		# Forbidden hashtags
		forbidden = tools.load_json(os.path.join(os.getcwd(), 'forbidden_hashtags.json'))
		forbidden = [str(i) for i in forbidden['hashtags']]

		driver = webdriver.Chrome()
		driver.maximize_window()
		driver.implicitly_wait(5)

		url = 'https://www.instagram.com/?hl=en'
		driver.get(url)

		# Access to log in page
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
		driver.implicitly_wait(5)
		# Log in task
		log = tools.load_json(os.path.join(os.getcwd(), 'info.json'))
		tools.login(driver, log)
		driver.implicitly_wait(5)

		# Search bar
		while True: #loop pour pick le hashtag randomly
			like_limit = random.randint(25, self.max_like_per_round)
			hashtag = random.choice(log['search'])
			# hashtags_dict_analysis['searched_hashtags'][hashtag] = {}

			search = driver.find_element_by_css_selector('input[placeholder="Search"]')  # find Search bar
			search.send_keys(hashtag)
			driver.implicitly_wait(5)

			# Click on first link
			driver.find_element_by_xpath(
				'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').click()
			driver.implicitly_wait(5)

			# Click on 'Load More'
			try:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				driver.find_element_by_link_text('Load more').click()
			except NoSuchElementException:
				pass

			# Click on first photo
			first_photo_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]/a'
			first_photo = driver.find_element_by_xpath(first_photo_xpath)
			ActionChains(driver).move_to_element(first_photo).perform()  # remonter vers la 1er image de 'Most recent'

			count_row_scroll = 0
			# hashtag_count = 1
			try:
				row = 1
				while True: # tant qu'on peut scroll
					count_row_scroll += 1
					for col in [1, 2, 3]:
						col = str(col)
						image_i_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[' + str(row) + ']/div[' + col + ']/a'
						image_i = driver.find_element_by_xpath(image_i_xpath)
						ActionChains(driver).move_to_element(image_i).perform()
						image_i.click()

						username_xpath = '/html/body/div[3]/div/div/div[2]/div/article/header/div[2]/div[1]/div/a'
						username = driver.find_element_by_xpath(username_xpath).get_attribute('title')
						if 'shop' in username:  # TODO A RETRAVAILLER
							pass
						else:
							caption_xpath = '/html/body/div[3]/div/div/div[2]/div/article/div[2]/div[1]/ul/li'
							caption = driver.find_element_by_xpath(caption_xpath).text

							# Get hashtags with regex
							# hashtags_ = re.findall(r"#(\w+)", caption)
							# hashtags_ = list(set(hashtags_))
							# any_in = lambda a, b: bool(set(a).intersection(b))  # intersection between 2 lists
							# if any_in(forbidden, hashtags_):
							#     pass
							# else:
								# hashtags_dict_analysis['searched_hashtags'][hashtag] = hashtags_
								# hashtag_count += 1
								# Follow, like
							try:  # a mettre dans le else
								if driver.find_element_by_xpath("//button[contains(.,'Following')]"):
									print(username + 'is already followed')
							except NoSuchElementException:
								driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()
								time.sleep(random.uniform(0.2, 0.8))
								try:
									driver.find_element_by_xpath("//span[contains(.,'Like')]").click()
									like_count += 1
									# hashtag_count += 1
								except NoSuchElementException:  # if already liked [contains(., 'Unlike)]
									pass
							finally:
								time.sleep(random.uniform(0.2, 0.8))
								driver.find_element_by_xpath("//button[contains(.,'Close')]").click()
								driver.implicitly_wait(5)

					# Scroll down
					if count_row_scroll == 4:  # 1 new load = 4 lignes de charger
						driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						time.sleep(random.uniform(0.3, 0.8))
						count_row_scroll = 0

					row += 1

					if like_count == like_limit:  # tous les X likes, stop
						stop_ = random.uniform(20, 45)
						print(time.localtime(), stop_)
						time.sleep(60 * stop_)
						like_limit = random.randint(25, self.max_like_per_round)
						print('Onto the next : %s' % (time.strftime('%d/%m/20%y_%H:%M:%S', time.localtime())))

			except NoSuchElementException:  # if no more image
				pass  # look for another hashtag in search bar

			if time.localtime()[7] == self.start[7]  : #si meme jour
				if time.localtime()[3] == self.start[3] + 10:
					self.restart()
			else:
				self.restart()


if __name__ == "__main__":
	fire.Fire(Main)
