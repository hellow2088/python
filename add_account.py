# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import login
import read

class AddAccount(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2.5)
        self.base_url = "http://monitor.test.lxland.com"
        
    def test_add_account(self):

        driver = self.driver
        driver.get(self.base_url + "/user/login")
        login.login('admin','admin888',self.driver)
        driver.find_element_by_link_text(u'账户管理').click()
        time.sleep(1)
        '''*******************************读——取——文——件*************************************************'''
        l = read.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx','add_acc')
        time.sleep(5)
        # print (l[2]['test_case'])
        '''*******************************循——环——测——试**************************************'''
        d = []
        for i in range(len(l)):
            driver.find_element_by_id("btn-add-account").click()
            time.sleep(0.5)
            driver.find_element_by_id("userName").send_keys(l[i]['userName'])
            driver.find_element_by_id("userRealName").send_keys(l[i]['userRealName'])
            driver.find_element_by_id("userTelphone").send_keys(l[i]['userTelphone'])
            time.sleep(0.5)
            driver.find_element_by_id("userEmail").send_keys(l[i]['userEmail'])
            Select(driver.find_element_by_id("add-second-select")).select_by_visible_text(l[i][u'分公司'])
            time.sleep(0.3)
            Select(driver.find_element_by_id("add-third-select")).select_by_visible_text(l[i][u'部门'])
            Select(driver.find_element_by_id("add-limit")).select_by_visible_text(l[i][u'角色'])
            time.sleep(0.3)
            driver.find_element_by_id("btn-submit").click()
            time.sleep(1)

        
        
            '''************************弹——窗——验——证**************************************************'''
        
            alert = driver.find_element_by_id("doalert")
           

            if alert.is_displayed() == True:
                text1 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if text1 != l[i]['assert']:
                    d.append(i+2)
                print ('%d:%s'%(i+2,text1)),
                print (u'————————>'),
                print (l[i]['test_case'])
                print ('-----------------------------------------------')
                
                driver.find_element_by_id("doalert").click()
                time.sleep(1)


            '''************************添——加——页——面——验——证**************************************************'''
            submit = driver.find_element_by_id('btn-submit')
            h = 'xpath'
            w = "//span[@class='help-block small']"
            
            if submit.is_displayed() == True:
                if AddAccount.is_element_present(self,h,w) == True:
                    text2 = driver.find_element_by_xpath("//span[@class='help-block small']").text
                    if text2 != l[i]['assert']:
                        d.append(i+2)
                    print ('%d:%s'%(i+2,text2)),
                    print (u'————————>'),
                    print (l[i]['test_case'])
                    print ('-----------------------------------------------')
                
                driver.find_element_by_xpath("//button[@class='btn btn-default close-add-account']").click()
                time.sleep(1)

        print (d)


        '''***************************************验——证——函——数***********************************'''
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
