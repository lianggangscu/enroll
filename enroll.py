#!/usr/bin/env python
#encoding:utf-8 


from selenium import webdriver
import time

#the url for the target
url="http://www.gaokaoq.com/"

usrname="13688329270"
passwd="lwy0318"



def login(name=usrname,passwd=passwd):
    

    #generate a browser to access the web 
    driver = webdriver.Chrome()
    driver.get(url)

    #input the username and passwd
    driver.find_element_by_xpath("//*[@id='phone']").send_keys(name)
    driver.find_element_by_xpath("//*[@id='password']").send_keys(passwd)
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[2]/div[1]/form/div[4]/input").click()

    driver.implicitly_wait(10)
    #jump the grade page
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/ul/li[4]/a").click()

    #jump to the grade database page
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("/html/body/div[3]/ul[2]/li[1]/div[2]/div[2]/div/a").click()
    driver.implicitly_wait(10)
    
    #return the page
    return driver


def catergory(driver):

   

    nowhandle=driver.current_window_handle

    #jump to the grade page and there will get a new window
    driver.find_element_by_xpath("/html/body/div[3]/ul[2]/li[1]/div[2]/div[2]/div/a").click()
    driver.implicitly_wait(10)
    #temp=driver
    #science 系统默认是理科 
    #temp.find_element_by_xpath("/html/body/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/span[1]/a").click()


    allhandles=driver.window_handles
    for item in allhandles:
        if item!=nowhandle:
            driver.switch_to_window(item)
    #art
    temp=driver
    print(temp.title)
    #temp.find_element_by_xpath("/html/body/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/span[2]/a").click()
    time.sleep(10)
    





if __name__=="__main__":
    driver=login()
    catergory(driver)

