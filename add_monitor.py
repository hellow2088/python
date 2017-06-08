# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import login
import read

class AddMonitor(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://monitor.test.lxland.com/"
    
    def test_add_monitor(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        login.login('admin','admin888',self.driver)
        driver.find_element_by_link_text(u"功能配置").click()
        '''================================================'''
        l = read.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx','add_mo')

        for i in range(len(l)):
            driver.find_element_by_xpath("//button[@type='button']").click()
            time.sleep(0.5)
            driver.find_element_by_css_selector("input.confName").send_keys(l[i]['name'])
            time.sleep(0.5)
            driver.find_element_by_css_selector("input.speedLimit").send_keys(l[i]['speed'])
            time.sleep(0.5)
            Select(driver.find_element_by_css_selector('select.bytype')).select_by_visible_text(l[i]['type'])
            driver.find_element_by_css_selector("input.keywords").send_keys(l[i]['keywords'])
            time.sleep(0.5)
            driver.find_element_by_css_selector("canvas.amap-labels").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//button[2]").click()
            time.sleep(0.5)
            '''=========================================================='''
            save = driver.find_element_by_xpath("//button[2]")
            alert = driver.find_element_by_id("doalert")
            if save.is_displayed() == True:
                driver.find_element_by_xpath("(//button[@class='btn btn-default pull-left'])").click()
            elif alert.is_displayed() == True:
                driver.find_element_by_id("doalert").click()
            time.sleep(0.5)
    '''================================================================'''
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()