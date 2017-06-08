# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd

class ModifyUser(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://monitor.test.lxland.com/"
        
    
    def test_modify_user(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(1)

        driver.find_element_by_link_text(u"用户管理").click()
        
        time.sleep(0.5)

        d = []
        l = ModifyUser.read_file(self,'e:\\python\\vehicle\\data_vehicle.xlsx')
        # print l

        for i in range(len(l)):
            driver.find_element_by_id("keywords").clear()
            driver.find_element_by_id("keywords").send_keys(l[i]['target'])
            time.sleep(0.5)
            driver.find_element_by_id("doSearch").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//i[@title='修改']").click()

            driver.find_element_by_id("realname").clear()
            driver.find_element_by_id("mobile").clear()
            driver.find_element_by_id("card_no").clear()
            driver.find_element_by_id("address").clear()
            driver.find_element_by_id("email").clear()
            driver.find_element_by_id("plateNo").clear()
            time.sleep(0.5)

            driver.find_element_by_id("realname").send_keys(l[i]['realname'])
            time.sleep(0.5) 
            driver.find_element_by_id("mobile").send_keys(l[i]['mobile'])
            time.sleep(0.3)
            driver.find_element_by_id("card_no").send_keys(l[i]['card_no'])
            time.sleep(0.5)
            driver.find_element_by_id("address").send_keys(l[i]['address'])
            time.sleep(0.5)
            driver.find_element_by_id("email").send_keys(l[i]['email'])
            time.sleep(0.3)
            if len(l[i]['frameNo'])>0:
                driver.find_element_by_id("frameNo").click()
                time.sleep(0.5)
                driver.find_element_by_id("searchFrame").click()
                time.sleep(0.3)
                driver.find_element_by_id("searchFrame").send_keys(l[i]['frameNo'])
                time.sleep(1)
                driver.find_element_by_id('searchFrame').send_keys(Keys.HOME)
                time.sleep(0.5)
                driver.find_element_by_link_text(l[i]['frameNo']).click()
            time.sleep(0.3)
            driver.find_element_by_id("plateNo").clear()
            driver.find_element_by_id("plateNo").send_keys(l[i]['plateNo'])
            time.sleep(0.5)
            driver.find_element_by_id("btn-confirm").click()
            time.sleep(0.5)
            '''================================================================='''
        
            submit = driver.find_element_by_id('btn-confirm')
            alert = driver.find_element_by_id('doalert')

            # print (submit.is_displayed())
            # print (alert.is_displayed())

            if alert.is_displayed() == True:#先判断提示窗口是否存在
                t2 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if t2 !=l[i]['assert']:#如果提示与断言不一致，则第i个执行有问题，把序号存入列表
                    d.append(i+2)
                print ('%d::%s' % (i+2,t2))
                print (u'——————————>>%s' % l[i]['case'])
                print
                driver.find_element_by_id('doalert').click()
                time.sleep(1)
                if submit.is_displayed() == True:
                    driver.find_element_by_xpath("//button[@class='btn btn-default close-add-account']").click()
                    time.sleep(0.5)


            if submit.is_displayed() == True:#如果添加页面存在，则关闭添加窗口
                tip = driver.find_element_by_xpath("//span[@class='help-block small']").is_displayed()

                if tip == True:
                    t1 = driver.find_element_by_xpath("//span[@class='help-block small']").text
                    if t1 !=l[i]['assert']:#如果提示与断言不一致，则第i个执行有问题，把序号存入列表
                        d.append(i+2)
                    print ('%d::%s' % (i+2,t1))
                    print (u'——————————>>%s' % l[i]['case'])
                    print
                driver.find_element_by_xpath("//button[@class='btn btn-default close-add-account']").click()
                time.sleep(0.8)

        print (d)
                
    '''=================================================================='''

    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('modify_user')
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
