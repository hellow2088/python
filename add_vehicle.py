# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import login,read

class AddVehicle02(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
        self.base_url = "http://monitor.test.lxland.com/"
      
    
    def test_add_vehicle02(self):

        driver = self.driver
        driver.get(self.base_url + "/user/login")
        login.login('admin','admin888',self.driver)


        driver.find_element_by_link_text(u"车辆管理").click()
        time.sleep(0.3)
        '''
        1.重复添加
        2.车架号空
        3.车型空
        4.车架号不足17位
        5.设备号小于17位
        6.设备号重复
        7.重复车牌号
        8.车架号特殊字符
        9.设备号特殊字符

        '''

        l = read.read_file(self,'E:\\python\\vehicle\\data_vehicle.xlsx','add_vehicle')
        
        for i in range(len(l)):
            driver.find_element_by_id("btn-add-account").click()
            driver.find_element_by_xpath("(//input[@name='add'])[2]").click()
            time.sleep(0.3)
            driver.find_element_by_id("addFrameNo").send_keys(l[i]['frameNo'])
            driver.find_element_by_id("addDeviceNo").send_keys(l[i]['deviceNo'])
            driver.find_element_by_id("addPlateNo").send_keys(l[i]['PlateNo'])
            time.sleep(0.5)
            driver.find_element_by_id("addVtype").send_keys(l[i][u'车型'])
            time.sleep(0.5)
            driver.find_element_by_link_text(l[i][u'车型']).click()
            time.sleep(0.5)
            # driver.find_element_by_id("addPlateNo").click()
            time.sleep(0.5)
            Select(driver.find_element_by_id("add-second-select")).select_by_visible_text(l[i][u'分公司'])
            time.sleep(0.3)
            Select(driver.find_element_by_id("add-third-select")).select_by_visible_text(l[i][u'部门'])
            time.sleep(0.3)

            driver.find_element_by_id("btn-submit").click()
            time.sleep(0.3)

            '''**********************************************************************'''

            e = driver.find_element_by_id('doalert')
            

            if e.is_displayed() == True:#如果 弹窗存在
                text = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/p").text
                print ('%d::%s' % (i+2,text)),
                print (u'----------------------->%s' % l[i]['tc'])
                print
                driver.find_element_by_id("doalert").click()
                
            f1 = driver.find_element_by_id('btn-submit')#提交按钮
            if f1.is_displayed() == True:#如果 添加车辆页面提交按钮存在
                xp="//span[@class='help-block small']"
                locate='xpath'

                al = AddVehicle02.is_element_present(self,locate,xp)
                if al == True:
                    t5 = driver.find_element_by_xpath(xp).text
                    print ('%d::%s'% (i+2,t5)),
                    print (u'----------------------->%s' % l[i]['tc'])
                    print
                driver.find_element_by_xpath("//button[@class='btn btn-default close-add-account']").click()#关闭添加页面
            time.sleep(0.5)
                
    '''******************************************************************************'''

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True


    def tearDown(self):
        self.driver.quit()
       

if __name__ == "__main__":
    unittest.main()
