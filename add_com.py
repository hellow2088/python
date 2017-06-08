# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest,time,re,xlrd

class AddCom(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_add_com(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        driver.find_element_by_link_text(u"账户管理").click()
        time.sleep(0.3)
        driver.find_element_by_link_text(u"组织管理").click()
        time.sleep(1)
        '''======================================================'''
        l = AddCom.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')

        # alert = driver.find_element_by_id('doalert')
        for i in range(len(l)):
            driver.find_element_by_id("second-name").clear()
            driver.find_element_by_id("second-name").send_keys(l[i]['com'])
            driver.find_element_by_id("btn-add-second").click()
            time.sleep(0.3)
            alert = driver.find_element_by_id('doalert')
            if alert.is_displayed() == True:
                text = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                print(text)
                self.assertTrue(u"分公司名称重复",driver.find_element_by_xpath("//div[@class='modal-body']/p"))
                driver.find_element_by_id("doalert").click()
                time.sleep(0.5)
        for i in range(len(l)):
            driver.refresh()
            time.sleep(0.5)
            driver.find_element_by_css_selector("span.thirdName").click()
            time.sleep(0.3)
            driver.find_element_by_css_selector("div.editorline.editoring > span.editor > input[type=\"text\"]").send_keys(l[i]['part'])
            driver.find_element_by_xpath("//ul[@id='branch_list']/li/ul/li/div/span[2]/button").click()
            time.sleep(0.3)
            alert2 = driver.find_element_by_id('doalert')
            if alert2.is_displayed() == True:
                text2 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                print(text2)
                self.assertTrue(u"部门名称重复", driver.find_element_by_xpath("//div[@class='modal-body']/p"))
                driver.find_element_by_id("doalert").click()
                time.sleep(0.3)
    '''=========================================================================='''
    def read_file(self,file):
            f1 = xlrd.open_workbook(file)
            st = f1.sheet_by_name('add_com')
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
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
