# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Bind(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2.5)
        self.base_url = "http://monitor.test.lxland.com/"
        
    
    def test_bind(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        driver.find_element_by_link_text(u"车辆管理").click()
        driver.find_element_by_id('keywords').send_keys('TESTABCD123456700')
        time.sleep(0.5)
        driver.find_element_by_id('doSearch').click()
        time.sleep(0.3)


        l = [u'1asddSD@#￥￥d你好','TESTABCD123456700','TESTABCD1234']
        print (len(l))
        for i in range(len(l)):
            driver.find_element_by_xpath("//td[9]/i").click()
            time.sleep(0.3)

            alert = driver.find_element_by_id('doalert')
            if alert.is_displayed() == True:
                driver.find_element_by_id('doalert').click()
                time.sleep(0.3)
                driver.find_element_by_xpath("//td[9]/i").click()
                time.sleep(0.3)

            driver.find_element_by_id("registerDeviceNo").send_keys(l[i])
            time.sleep(0.3)
            driver.find_element_by_id("btn-confirm-bind").click()
            time.sleep(0.3)

            confirm = driver.find_element_by_id('btn-confirm-bind')

            if confirm.is_displayed() == True:
                driver.find_element_by_xpath("(//button[@type='button'])[7]").click()
                time.sleep(0.5)
        
    
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
