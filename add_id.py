# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time

import login,read

class AddId(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
        
    def test_add_id(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        login.login('admin','admin888',self.driver)
        driver.find_element_by_link_text(u"功能配置").click()
        time.sleep(0.5)
        driver.find_element_by_link_text(u"车辆ID定义").click()
        time.sleep(0.5)
        '''========================================================='''

        l = read.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx','function')

        for i in range(len(l)):
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            if len(l[i]['id'])==0:
                break
            driver.find_element_by_css_selector("input.form-control.paramId").send_keys(l[i]['id'])
            time.sleep(0.3)
            Select(driver.find_element_by_css_selector("select.partId.form-control")).select_by_visible_text(l[i][u"选择零部件"])
            time.sleep(0.3)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            time.sleep(0.5)

            a = driver.find_element_by_id('doalert')
            print (a.is_displayed())
            if a.is_displayed() == True:
                # self.assertEqual(u"<i class=\"fa fa-warning text-warning\"></i> 以存在相同车辆Id", self.close_alert_and_get_its_text())
                driver.find_element_by_id("doalert").click()
                time.sleep(1)

           
    '''=============================================================='''
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
       

if __name__ == "__main__":
    unittest.main()
