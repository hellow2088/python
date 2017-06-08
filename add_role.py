# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd

class AddRole(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://monitor.test.lxland.com/"
        
    
    def test_add_role(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        '''======================================================='''
        driver.find_element_by_link_text(u"账户管理").click()
        time.sleep(0.6)
        driver.find_element_by_link_text(u"角色权限").click()
        time.sleep(0.6)
        

        l = AddRole.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')
        # print l
        
        for i in range(len(l)):
            driver.find_element_by_link_text(u"添加角色").click()
            time.sleep(0.6)
            driver.find_element_by_id("roleName").send_keys(l[i]['role'])
            driver.find_element_by_id("allcheck").click()
            time.sleep(0.5)
            driver.find_element_by_id("btn-submit").click()
            time.sleep(0.5)

            alert = driver.find_element_by_id('doalert')
            if alert.is_displayed() == True:
                text_alert = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if l[i]['assert'] == text_alert:
                    print ('%d>>%s'% (i+2,l[i]['tc'])),
                    print (u'——————————>>%s'% l[i]['assert'])
                    driver.find_element_by_id('doalert').click()
                    time.sleep(0.5)
                    driver.find_element_by_link_text(u'返回').click()
                    time.sleep(0.5)
                else:
                    print ('%d>>%s'% (i+2,l[i]['tc'])),
                    print (u'——————————>>%s'% l[i]['assert'])

        print ('==============================================================')




        for i in range(len(l)):
            driver.find_element_by_css_selector("i.fa.fa-edit").click()
            driver.find_element_by_id("roleName").clear()
            time.sleep(0.5)
            driver.find_element_by_id("roleName").send_keys(l[i]['role2'])
            time.sleep(0.5)
            driver.find_element_by_id("allcheck").click()
            time.sleep(0.5)
            driver.find_element_by_id("btn-submit").click()
            time.sleep(0.5)

            alert = driver.find_element_by_id('doalert')
            if alert.is_displayed() == True:
                text_alert = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if l[i]['assert'] == text_alert:
                    print ('%d>>%s'% (i+2,l[i]['tc'])),
                    print (u'——————————>>%s'% l[i]['assert'])
                    driver.find_element_by_link_text(u'返回').click()
                    time.sleep(0.5)
            else:
                print ('%d>>%s'% (i+2,l[i]['tc'])),
                print (u'——————————>>%s'% l[i]['assert'])

        for i in range(len(l)):
            driver.find_element_by_css_selector("i.fa.fa-trash").click()
            time.sleep(0.5)
            driver.find_element_by_id('doalert').click()
            time.sleep(0.5)

        




    '''=============================================================='''
    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('role')
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
    
    def tearDown(self):
        self.driver.quit()
       

if __name__ == "__main__":
    unittest.main()
