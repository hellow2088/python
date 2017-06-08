# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd

class BindFno(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com"
    
    def test_bind_fno(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        driver.find_element_by_link_text(u'车辆管理').click()
        '''-----------------------------------------------------------------'''
        l = BindFno.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')
        d = []
        

        for i in range(len(l)):
            driver.find_element_by_id('keywords').clear()
            driver.find_element_by_id('keywords').send_keys(l[i]['target'])
            time.sleep(0.3)
            driver.find_element_by_id('doSearch').click()
            time.sleep(0.3)
            driver.find_element_by_xpath('//td[9]/i').click()

            alert = driver.find_element_by_id("doalert")
            if alert.is_displayed() == True:
                t1 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                '''
                如果已绑定，则解绑，再测试绑定
                已绑定，会提示是否需要解绑
                '''
                if t1 == u'确定要解绑吗?':
                    driver.find_element_by_id('doalert').click()
                    time.sleep(1)
                    driver.find_element_by_xpath('//td[9]/i').click()
                    time.sleep(0.3)
                    driver.find_element_by_id("registerDeviceNo").send_keys(l[i]['dno'])
                    time.sleep(0.3)
                    driver.find_element_by_id("btn-confirm-bind").click()
                    time.sleep(0.3)

            else:
                time.sleep(0.3)
                driver.find_element_by_id("registerDeviceNo").send_keys(l[i]['dno'])
                time.sleep(0.3)
                driver.find_element_by_id("btn-confirm-bind").click()
                time.sleep(0.3)

            '''---------------------------弹——窗-------------------------------------'''
        
            alert = driver.find_element_by_id("doalert")

            if alert.is_displayed() == True:
                t1 = driver.find_element_by_xpath("//div[@class='modal-body']/p").text
                if t1 != l[i]['assert']:
                    d.append(i+2)
                    
                print ('%d::%s' % (i+2,t1)),
                print (u'——————————————>%s' % l[i]['tc'] )
                print

                driver.find_element_by_id("doalert").click()
                time.sleep(0.5)
            '''---------------------------页——面——提——醒-------------------------------------'''
            btn = driver.find_element_by_id('btn-confirm-bind')
            if btn.is_displayed() == True:
                h = 'xpath'
                w = "//span[@class='help-block small']"
                t = BindFno.is_element_present(self,h,w)
                #如果绑定页面存在，再次判断是否存在 页面提示
                #如果存在，则提取提示，并与断言比较
                if t == True:
                    t2 = driver.find_element_by_xpath("//span[@class='help-block small']").text
                    if t2 != l[i]['assert']:
                        d.append(i+2)
                    print ('%d::%s' % (i+2,t2)),
                    print (u'——————————————>%s'% l[i]['tc'])
                    print
                    driver.find_element_by_xpath("(//button[@type='button'])[7]").click()
                    time.sleep(1)
                else:
                    driver.find_element_by_xpath("(//button[@type='button'])[7]").click()
                    time.sleep(1)
        print (d)


    '''----------------------------------------------------------------'''
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('bind_dnu')
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

    
    # def tearDown(self):
    #     #self.driver.quit()
       
if __name__ == "__main__":
    unittest.main()
