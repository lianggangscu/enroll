#!/usr/bin/env python
#encoding:utf8



from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

import pickle

url='https://www.cdzk.cn'
#usrname="13688329270" #science
usrname="13518151051"
passwd="lwy0318"



def login(Url=url,usrname=usrname,passwd=passwd):
    '''
    模拟登陆金榜题名
    :param Url:
    :param usrname:
    :return:
    '''

    #access the homepage
    driver=webdriver.Chrome()
    driver.get(Url)
    driver.implicitly_wait(10)


    #get the login element, and a new window will jump
    driver.find_element_by_xpath('//*[@id="bs-navbar"]/ul[1]/li/a').click()
    driver.implicitly_wait(10)
    windows=driver.window_handles
    newWin=windows[-1]
    driver.switch_to_window(newWin)
    driver.implicitly_wait(10)


    #input the usrname and passwd
    driver.find_element_by_xpath('//*[@id="tel"]').send_keys(usrname)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="subMitLogin"]').click()
    driver.implicitly_wait(10)


    #jump to the page for score query page
    driver.find_element_by_xpath('//*[@id="tog"]/div[4]/div[2]/ul[2]/li[3]/a').click()
    driver.implicitly_wait(10)


    #jump to the page for score
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/a[3]').click()
    driver.implicitly_wait(10)

    #time.sleep(10)

    return driver


def getPages(driver):
    '''
    get the total page for  the task
    :param driver:
    :return:
    '''

    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/ul/li[13]').click()
    driver.implicitly_wait(10)
    pages=int(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/ul/li[11]').text)
    print("total:{0} pages".format(pages))

    #back to the frist page
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/a[3]').click()
    driver.implicitly_wait(10)

    return pages

def getProgress(filename="progress.txt"):

    progress=0

    with open("progress.txt") as f:
        progress=f.read()
        if progress==None:
            progress=0


    return int(progress)

def parsePages(driver,pages,page=0):
    '''
    #解析页面，获取网页内容
    :param driver:
    :param pages:
    :return:
    '''

    tasks=[]
    count=0
    pageNum=int(pages) #the total page for page num

    if page>=pages:
        driver.close()
        return
    if page!=0:
        for item in range(page-1):
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/ul/li[12]').click()
            driver.implicitly_wait(10)
    count=page

    while(count<=pages):
        count+=1 #page one
        parsePage(driver,tasks)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/ul/li[12]').click()
        driver.implicitly_wait(10)
        with open("progress.txt",'w') as f:
            f.write(str(count))

    driver.close()

    with open("art.txt",'w') as f:
        pickle.dump(tasks, f)

    return tasks






def parsePage(driver,tasks):
    '''
    解析一张页面内容
    :param driver:
    :return:
    '''


    print("parse page")

    #第一个元素
    try:
        # collegeNames=driver.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[1]')
        # collegePros=driver.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[2]')
        # cater=driver.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[3]')
        # enrollType=driver.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[4]')
        detailLinks=driver.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[5]/a')
    except Exception,e:
        print(e)
        return


    count=len(detailLinks)

    for item in range(count):
        # name=collegeNames[item].text
        # pro=collegePros[item].text
        # cat=cater[item].text
        # eno=enrollType[item].text
        # print(name,pro,cat,eno)
        task=parseUrl(detailLinks[item])
        tasks.append(task)
    #getData(tasks)





def parseUrl(urlEle):
    '''
    解析链接获取全部数据
    :param urlEle: 
    :return: 
    '''
    onetask=[]


    urlstring=urlEle.get_attribute("onclick")
    datalists=urlstring.split(',')
    for index, item in enumerate(datalists):
        if index==0:
            url=item.split('(')[-1]
            print(url)
            onetask.append(url.split("'")[1])
        elif index==3:
            type=item.split(')')[0]
            print(type)
            onetask.append(type.split("'")[1])
        else:
            print(item)
            onetask.append(item.split("'")[1])

        return onetask




def simLogin(url=url):
    bro = webdriver.Chrome()

    bro.get(url)

    bro.find_element_by_xpath('//*[@id="bs-navbar"]/ul[1]/li/a').click()
    bro.implicitly_wait(10)
    windows = bro.window_handles
    newWin = windows[-1]
    bro.switch_to_window(newWin)
    bro.implicitly_wait(10)

    bro.find_element_by_xpath('//*[@id="tel"]').send_keys(usrname)
    bro.find_element_by_xpath('//*[@id="pwd"]').send_keys(passwd)
    bro.find_element_by_xpath('//*[@id="subMitLogin"]').click()
    bro.implicitly_wait(10)

    return bro

def getData(tasks):
    '''
    get the real data and save to db
    :param tasks:
    :return:
    '''

    bro=simLogin(url)


    #bro=webdriver.Chrome()
    for item in tasks:
        print(item)
        finurl=url+item[0]
        print(finurl)



        #create a new tab
        # bro.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
        # bro.implicitly_wait(10)
        # bro.switch_to().window(tabs.get(1)) # switches to new tab

        bro.get(finurl)

        bro.implicitly_wait(10)











if __name__=="__main__":
    driver=login()
    #parsePage(driver)
    pages=getPages(driver)
    progress=getProgress()
    print(progress)
    tasks=parsePages(driver,pages,progress)
    for item in tasks:
        print(item)