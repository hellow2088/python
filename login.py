# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd



def login(name,pw,driver):
	driver.implicitly_wait(3)
	driver.maximize_window()
	driver.find_element_by_id('userName').send_keys(name)
	time.sleep(0.3)
	driver.find_element_by_id('userPwd').send_keys(pw)
	time.sleep(0.3)
	driver.find_element_by_id('captcha').send_keys('0000')
	driver.find_element_by_id('submit').click()
	time.sleep(3)
