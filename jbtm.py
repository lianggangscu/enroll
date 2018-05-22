#!/usr/bin/env python
#encoding:utf8



from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

import pickle
import time
import  MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')
url='https://www.cdzk.cn'
#usrname="13688329270" #science
usrname="13518151051" #art
passwd="lwy0318"


def login(url):
    '''
    模拟登陆网站首页
    :param url:
    :return: 返回页面的driver

    '''

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

def entenProPage(driver):
    '''
    进入到分数查询页面
    :param bro:
    :return:
    '''

    driver.find_element_by_xpath('//*[@id="tog"]/div[4]/div[2]/ul[2]/li[3]/a').click()
    driver.implicitly_wait(10)

    # jump to the page for score
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/a[3]').click()
    driver.implicitly_wait(10)

    # time.sleep(10)

    return driver


def getPages(bro):
    '''
    获取爬取专业的页数
    :param driver:
    :return:
    '''
    pageNum=0

    #获得学校的页数
    pages = bro.find_elements_by_xpath('//*[@id="pager"]/ul/li')
    length=len(pages)

    if (length==13):
        pages[-1].click()
        bro.implicitly_wait(10)
        pageNum=int(bro.find_elements_by_xpath('//*[@id="pager"]/ul/li')[-3].text)
    else:
        pageNum=int(pages[-3].text)

    #返回专业查询首页
    print("Totoal Pages:{0}".format(pageNum))
    bro.get(bro.current_url)
    bro.implicitly_wait(10)


    return (bro,pageNum)

def parsePage(bro,pageNum):
    '''
    对分数页面进行解析，获取相关数据，从页面获取身份，和最后的超链接获取相关信息
    :param bro:
    :param pageNum:
    :return:
    '''

    count=pageNum
    tasks=[]

    #对每一页进行循环，获取每一页的信息

    for item in range(count):
        try:
            collegePros=bro.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[2]')
            detailLinks=bro.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[5]/a')
        except Exception,e:
            print(e)
            return


        #对每一页的数据进行处理，获得学校所在省名
        cnt = len(detailLinks)
        for item in range(cnt):
            # name=collegeNames[item].text
            pro = collegePros[item].text
            # cat=cater[item].text
            # eno=enrollType[item].text
            # print(name,pro,cat,eno)
            print(pro)
            print(detailLinks[item].text)
            task = parseUrl(detailLinks[item], pro)
            tasks.append(task)



        bro.find_elements_by_xpath('//*[@id="pager"]/ul/li')[-2].click()
        bro.implicitly_wait(10)

    with open("art.txt","w") as f:
        pickle.dump(tasks,f)

def parseUrl(pageEle,pro):
    '''
    对页面进行解析，获取每个连接的信息
    :param pageEle:
    :param pro:
    :return:
    '''

    #返回的每个节点信息：链接，学校名，文理可，录取批次，身份
    onetask = []


    urlstring = pageEle.get_attribute("onclick")
    print(urlstring)

    #对字符串进行切分
    datalists = urlstring.split(',')
    print(datalists)

    for index, item in enumerate(datalists):
        if (index == 0):
            url = item.split("(")[1].split("'")[1]
            print(url)
            onetask.append(url)
        elif (index == 3):
            type = item.split(")")[0].split("'")[1]
            print(type)
            onetask.append(type)
        else:
            item = item.split("'")[1]
            onetask.append(item)

    onetask.append(pro)
    print(onetask)
    return onetask







if __name__=="__main__":
    bro=login(url)
    bro=entenProPage(bro)
    bro,pageNum=getPages(bro)
    parsePage(bro,pageNum)

