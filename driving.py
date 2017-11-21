# -*- coding: utf-8 -*-
import os
import re
import time
import shelve
import requests
import pytesseract
from PIL import Image
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --outputbase digits'

#init driver
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"  
os.environ["webdriver.chrome.driver"] = chromedriver  
driver = webdriver.Chrome(chromedriver)

try:
	###########################登录页面#############################################
	#input url
	loginUrl = "http://180.166.247.18:8082/dsp/manage/main/index.htm"
	driver.get(loginUrl)
	driver.maximize_window()

	user = driver.find_element_by_name("account")
	user.send_keys("07100094")  

	user = driver.find_element_by_name("password")
	user.send_keys("147179")

	img_path = 'D:\\png\\screenshot.png'
	driver.save_screenshot(img_path) # saves screenshot of entire page

	element = driver.find_element_by_tag_name("p").find_element_by_tag_name("img")

	location = element.location
	size = element.size
	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']

	im = Image.open(img_path) # uses PIL library to open image in memory
	im = im.crop((left, top, right, bottom)) # defines crop points
	im.save(img_path) # saves new cropped image

	#verify code
	img = Image.open(img_path)
	txt = pytesseract.image_to_string(img,config=tessdata_dir_config).replace(' ','').replace('.','')

	user = driver.find_element_by_name("checkCode")
	user.send_keys(txt)

	submit =  driver.find_element_by_tag_name("p").find_elements_by_tag_name("input")[1]
	submit.click()

	#############################选课页面#########################################
	driver.switch_to_frame("leftFrame");
	yuyue = driver.find_element_by_id("menu_bar_504")
	yuyue.click()

	xunlianyuyue = driver.find_element_by_id("active_menu").find_elements_by_tag_name("a")[3]
	xunlianyuyue.click()

	driver.switch_to_default_content()
	driver.switch_to_frame('centerFrame')
	targetDate = driver.find_element_by_id("targetDate")
	end_date = datetime.now()+ timedelta(days=15)
	targetDate.clear()
	targetDate.send_keys(datetime.strftime(end_date,'%Y-%m-%d'))

	refresh = driver.find_element_by_id("refresh")
	refresh.click()

	# driver.close()
	# driver.quit()
except Exception as e:
	raise e
finally:
	file = os.path.join("D:\\png\\", "screenshot.png")
	os.remove(file)

