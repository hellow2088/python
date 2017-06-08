# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd

class Service(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://monitor.test.lxland.com/"
        
    def test_service(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("admin888")
        driver.find_element_by_id("captcha").send_keys("0000")
        driver.find_element_by_id("submit").click()
        time.sleep(2)
        '''=============================================================='''

        driver.find_element_by_link_text(u"服务店管理").click()
        time.sleep(0.3)

        l = Service.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx')

        for i in range(len(l)):
            driver.find_element_by_id("btn-add-account").click()
            time.sleep(0.5)
            driver.find_element_by_id("storeName").send_keys(l[i][u'服务店名'])
            Select(driver.find_element_by_id("storeType")).select_by_visible_text(l[i][u'类型'])
            time.sleep(0.3)
            Select(driver.find_element_by_id("province")).select_by_visible_text(l[i][u'省'])
            time.sleep(0.3)
            Select(driver.find_element_by_id("city")).select_by_visible_text(l[i][u'市'])
            time.sleep(0.3)
            driver.find_element_by_id("district").click()
            time.sleep(0.3)
            Select(driver.find_element_by_id("district")).select_by_visible_text(l[i][u'区/县'])
            time.sleep(0.3)
            driver.find_element_by_css_selector("canvas.amap-vectors").click()
            time.sleep(0.3)
            # driver.find_element_by_id("storeAddr").send_keys(l[i][u'电话'])
            time.sleep(0.3)
            driver.find_element_by_id("storeTelphone").send_keys(l[i][u'电话'])
            time.sleep(0.3)
            driver.find_element_by_id("storeContact").send_keys(l[i][u'联系人'])
            time.sleep(0.3)
            driver.find_element_by_id("storePhone").send_keys(l[i][u'联系人电话'])
            time.sleep(0.3)
            driver.find_element_by_id("imgsrc").send_keys(l[i][u'图片'])
            time.sleep(2)
            driver.find_element_by_id("remark").send_keys(l[i][u'店内服务'])
            time.sleep(0.3)
            driver.find_element_by_id("doSave").click()
            time.sleep(0.3)
            '''==============================================================================================='''

            h = 'xpath'
            w = "//span[@class='help-block small']"
            t = Service.is_element_present(self,h,w)
            
            if t == True:
                t2 = driver.find_element_by_xpath("//span[@class='help-block small']").text
                if t2 != l[i]['assert']:
                    d.append(i+2)
                print ('%d::%s' % (i+2,t2)),
                print (u'——————————————>%s'% l[i]['tc'])
                print
                driver.find_element_by_link_text(u"取消").click()
                time.sleep(1)
            else:
                 driver.find_element_by_id("doalert").click()


           
    '''========================================================================================================='''
    def read_file(self,file):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name('service')
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
