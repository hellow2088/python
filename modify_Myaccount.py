# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd
class ModifyMyaccount(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
        
    
    def test_modify_myaccount(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("test00")
        driver.find_element_by_id("userPwd").send_keys("123456")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)

        '''**********************清——除——数——据***********************************'''
        driver.find_element_by_link_text(u'账户管理').click()
        time.sleep(0.5)
        driver.find_element_by_link_text(u"我的账户").click()
        time.sleep(0.5)
        

        '''**********************循——环——输——入***********************************'''
        l = ModifyMyaccount.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')
        #print l
        d = []

        for i in range(len(l)): 

            driver.find_element_by_link_text(u"我的账户").click()           
            
            time.sleep(1)
            driver.find_element_by_id("userName").clear()
            driver.find_element_by_id("userName").send_keys(l[i]['userName'])
            driver.find_element_by_id("userRealName").clear()
            driver.find_element_by_id("userRealName").send_keys(l[i]['userRealName'])
            driver.find_element_by_id("userTelphone").clear()
            driver.find_element_by_id("userTelphone").send_keys(l[i]['userTelphone'])
            time.sleep(0.5)
            driver.find_element_by_id("userEmail").clear()
            time.sleep(0.5)
            driver.find_element_by_id("userEmail").send_keys(l[i]['userEmail'])
            time.sleep(0.5)
            f9 = driver.find_element_by_id("doSave")
            if f9.is_displayed() == True:
                driver.find_element_by_id("doSave").click()

            # print f9.is_displayed()
            # driver.find_element_by_xpath("//button[@id='doSave']").click()
            time.sleep(0.5)
        


            '''**********************结——果——验——证************************************'''
            alert = driver.find_element_by_id('doalert')
            
            if alert.is_displayed() == True:
                t1 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if l[i]['assert'] != t1:
                    d.append(i+2)
                print ('%d::%s' % (i+2,t1)),
                print (u'——————————>>%s' % l[i]['case'])
                print
                driver.find_element_by_id("doalert").click()
            else:
                t2 = driver.find_element_by_xpath("//span[@class='help-block small']").text
                if l[i]['assert'] != t2:
                    d.append(i+2)
                print ('%d::%s' % (i+2,t2)),
                print (u'——————————>>%s' % l[i]['case'])
                print
        print (d)


        '''*********************************************************'''
    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('modify_Myaccount')
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
    

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
