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

def enterProPage(driver):
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


def getTask(fileName):
    '''
    获取任务列表
    :param filenName:
    :return:
    '''

    tasks=[]
    with file(fileName) as f:
        tasks=pickle.load(f)


    # for item in tasks:
    #     print item

    # print(len(tasks))
    return tasks


def getData(bro,prourl):
    '''
    获取页面的专业数据
    :param prourl:
    :return:

    '''
    #进入专业页面
    bro.get(prourl)
    bro.implicitly_wait(10)

    #通过xpath获取页面的元素
    try:
        collegeinfo=bro.find_element_by_xpath('/html/body/div/p').text
        #print(collegeinfo)
        collegename,cater,enterorder,proname=parseCollege(collegeinfo)
        #获取成绩
        years=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/th')
        scores=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[1]')
        diffs=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[2]')
        ranks=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[3]')
        avers=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[4]')
        averdiffs=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[5]')
        averranks=bro.find_elements_by_xpath('/html/body/table/tbody/tr[position()>0]/td[6]')

        leng=len(years)

        for item in range(leng):
            year=years[item].text
            score=scores[item].text
            diff=diffs[item].text
            rank=ranks[item].text
            aver=avers[item].text
            averdiff=averdiffs[item].text
            averrank=averranks[item].text

            print(collegename, cater, enterorder, proname, year, score, diff, rank, aver, averdiff, averrank)
            save2db(collegename,cater,enterorder,proname,year,score,diff,rank,aver,averdiff,averrank)

    except Exception,e:
        print e
        return None








def parseCollege(string):
    '''
    对学校信息进行解析
    :param string:
    :return:
    '''
    strLists=string.split("：")
    #print(strLists)
    collegename=strLists[1].encode('gb2312')
    collegename =collegename[:-4]
    collegename=collegename.decode('gb2312')
    cater=strLists[2].split(" ")[0]
    enterorder = strLists[3].split(" ")[0]
    proname=strLists[4].split(" ")[0]

    return (collegename,cater,enterorder,proname)

def save2db(collegename,cater,enterorder,proname,year,score,diff,rank,aver,averdiff,averrank):
    '''
    将数据存入数据库
    :return:
    '''

    #连接到数据库
    db= MySQLdb.connect("localhost", "root", "lianglove3", "chiyuan", charset='utf8' )

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句

    sql="insert into protable(collegename,cater,enterorder,proname,year,score,diff,rank,avescore,avediff,averank)\
        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
        %(collegename,cater,enterorder,proname,year,score,diff,rank,aver,averdiff,averrank)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception,e:
        # 发生错误时回滚
        print(e)
        db.rollback()

    # 关闭数据库连接
    db.close()

if __name__=="__main__":
    bro=login(url)
    #enterProPage(bro)

    #理科专业页面链接
    tasks=getTask("sciencepro.txt")

    for item in tasks:
        getData(bro,item)


    #文科专业页面链接
    tasks=getTask("artpro.txt")
    for item in tasks:
        getData(bro,item)