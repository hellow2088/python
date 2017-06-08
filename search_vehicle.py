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


class SearchVehicle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
       
    
    def test_search_vehicle(self):
        driver = self.driver
        driver.get(self.base_url + "/user/login")
        driver.maximize_window()
        login.login('admin','admin888',self.driver)
        time.sleep(2)
        '''==============================================================='''
        l = read.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx','search_vehicle')
        '''
        全部车辆查询，没有车型查询条件
        当循环到车型查询条件时，跳出循环

        '''
        driver.find_element_by_id('searchSingle').click()
        for i in range(len(l)):
            if l[i]['searchType'] == u'车型':
                break
            Select(driver.find_element_by_css_selector("select.bytype")).select_by_visible_text(l[i]['searchType'])
            time.sleep(0.3)
            driver.find_element_by_css_selector('input.keywords').clear()
            time.sleep(0.3)
            driver.find_element_by_css_selector('input.keywords').send_keys(l[i]['target'])
            time.sleep(0.3)
            driver.find_element_by_css_selector('button.search').click()
            time.sleep(0.5)
            
            t = driver.find_element_by_xpath("//form[@class='control-search-form']").text
            if l[i]['for_single_click'] in t:
                print ('find')
            else:
                print(u'没找到：%s' % l[i]['for_single_click'])
        '''======================================================================'''

        driver.find_element_by_link_text(u"单车监控").click()

        for i in range(len(l)):
            print(i+2)
            if l[i]['searchType'] == u'车型':
                break
            Select(driver.find_element_by_id("bytype")).select_by_visible_text(l[i]['searchType'])
            time.sleep(0.5)
            '''
            如果查询条件时车牌号，则截取字符串
            '''
            if l[i]['searchType'] == u'车牌号':
                l1 = l[i]['target'][1:7]
                l2=l[i]['target'][0]
                print(l2)
                print(l1)

                driver.find_element_by_id('plateNo').click()
                time.sleep(0.3)
                driver.find_element_by_link_text(l2).click()
                time.sleep(0.5)
                driver.find_element_by_id("keywords").clear()
                driver.find_element_by_id("keywords").send_keys(l[i]['target'][1:7])
                time.sleep(0.5)
                driver.find_element_by_id("doSearch").click()
                time.sleep(0.5)

                alert = driver.find_element_by_id('doalert')
                print(alert.is_displayed())
                if alert.is_displayed() == True:
                    driver.find_element_by_id('doalert').click()
                    time.sleep(0.5)

            driver.find_element_by_id("keywords").send_keys(l[i]['target'])
            time.sleep(0.5)
            '''
            不是车牌号，且长度小于17，是模糊查询，点击模糊提示
            '''
            if l[i]['searchType']!=u'车牌号' and len(l[i]['target']) < 17:
                driver.find_element_by_link_text(l[i]['for_single_click']).click()
                time.sleep(0.3)



        '''================================================================'''
        driver.find_element_by_link_text(u"车辆管理").click()

        

        for i in range(len(l)):
            Select(driver.find_element_by_id("bytype")).select_by_visible_text(l[i]['searchType'])
            driver.find_element_by_id("keywords").clear()
            time.sleep(0.3)
            driver.find_element_by_id("keywords").send_keys(l[i]['target'])
            time.sleep(0.3)
            driver.find_element_by_id("doSearch").click()
            time.sleep(0.5)
       
        '''============================历史数据--查询======================================'''

        driver.get('http://monitor.test.lxland.com/vehicle-monitor/history')
        time.sleep(2)
        for i in range(len(l)):
            print(i+2)
            if l[i]['searchType'] == u'车型':
                break
            Select(driver.find_element_by_id("bytype")).select_by_visible_text(l[i]['searchType'])
            time.sleep(0.5)
            '''
            如果查询条件时车牌号，则截取字符串
            '''
            if l[i]['searchType'] == u'车牌号':
                l1 = l[i]['target'][1:7]
                l2=l[i]['target'][0]
                # l[i]['target'] = l1
                print(l2)
                print(l1)

                driver.find_element_by_id('plateNo').click()
                time.sleep(0.5)
                driver.find_element_by_link_text(l2).click()
                time.sleep(0.3)
                driver.find_element_by_id("doSearch").click()

                driver.find_element_by_id("keywords").clear()
                time.sleep(0.3)
                driver.find_element_by_id("keywords").send_keys(l[i]['target'][1:7])
                time.sleep(0.5)

            else:
                driver.find_element_by_id("keywords").clear()
                time.sleep(0.3)
                driver.find_element_by_id("keywords").send_keys(l[i]['target'])
                time.sleep(0.5)
            '''
            不是车牌号，且长度小于17，是模糊查询，点击模糊提示
            '''
            if l[i]['searchType']!=u'车牌号' and len(l[i]['target']) < 17:
                 driver.find_element_by_link_text(l[i]['for_single_click']).click()
            time.sleep(0.3)
            driver.find_element_by_id("doSearch").click()
            time.sleep(1)
            self.assertTrue(l[i]['for_single_click'],driver.find_element_by_xpath("//div[@class='box-body']"))
            time.sleep(1)
       



    '''================================================================================='''
    
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
