# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,xlrd

class AddUnit(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
       
    def test_add_unit(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        '''========================================================'''
        driver.find_element_by_link_text(u"功能配置").click()
        time.sleep(0.3)
        driver.find_element_by_link_text(u"零部件定义").click()
        time.sleep(0.3)

        l = AddUnit.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')

        for i in range(len(l)):
            driver.find_element_by_xpath("//button[@type='button']").click()
            time.sleep(0.3)
            driver.find_element_by_css_selector("input.form-control.name").send_keys(l[i][u'零部件'])
            time.sleep(0.3)
            driver.find_element_by_css_selector("input.form-control.shortName").send_keys(l[i][u'缩写'])
            time.sleep(0.3)
            driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
            time.sleep(0.5)

            b = driver.find_element_by_xpath("(//button[@type='button'])[3]")
            if b.is_displayed() == True:
                driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
                time.sleep(0.5)
            # f = self.assertTrue(l[i][u'零部件'],driver.find_element_by_xpath("//div[@class='box-body']"))
            # if f == False:
            #     driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            #     time.sleep(0.5)

            # driver.find_element_by_xpath("//button[@type='button']").click()
            # driver.find_element_by_css_selector("input.form-control.name").clear()
            # driver.find_element_by_css_selector("input.form-control.name").send_keys(u"零部件")
            # driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
            # driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    
    '''======================================================================'''

    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('function')
        nr = st.nrows
        cn = st.row_values(0)

        list = []

        for i in range(1,nr):
            r = st.row_values(i)
            app = {}
            for i in range(0,len(cn)):
                app[cn[i]] = r[i]

            list.append(app)
        return list
        print (len(list[1]))
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
