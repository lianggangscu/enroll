#!/usr/bin/env python
#encoding:utf-8
from _threading_local import local

from selenium import webdriver
import time
import  MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
   # driver.find_element_by_xpath("/html/body/div[3]/ul[2]/li[1]/div[2]/div[2]/div/a").click()
   # driver.implicitly_wait(10)
    
    #return the page
    return driver


def catergory(driver):

   

    nowhandle=driver.current_window_handle

    #jump to the grade page and there will get a new window
    driver.find_element_by_xpath("/html/body/div[3]/ul[2]/li[1]/div[2]/div[2]/div/a").click()
    driver.implicitly_wait(10)

    caterWindows =driver.window_handles
    mainWindow=caterWindows[0]
    newWindow=caterWindows[1]

    #science page
    driver.switch_to_window(newWindow)#jump to the databases page

    #以年来循环
    #文科
    driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/span[2]/a").click()
    driver.implicitly_wait(10)
    years=getYear(driver)
    yearNum=len(years)
    for count in range(yearNum):
        item=getYear(driver)[count]
        print("year:",item.text)
        item.click()
        driver.implicitly_wait(10)
        #print("year:",item.text)

        #获取地点信息
        local=getLocation(driver)
        locNum=len(local)

        for loccount in range(locNum):
            item=getLocation(driver)[loccount]
            loc=item.text
            item.click()
            driver.implicitly_wait(10)
            pages(driver,loc)

    


    #Jump to art page
    #driver.switch_to_window(newWindow)
    # print(driver.title)
    #driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/span[2]/a").click()
    #time.sleep(10)
    


def getLocation(driver):
    '''
    获取地名
    '''
    links=driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/table/tbody/tr[3]/td[2]/span[position()>1]/a')
    #texts=driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/table/tbody/tr[3]/td[2]/span[position()>1]/a').text

    # for item in links:
    #     print(item)
    #     print(item.text)

    return links


def getYear(driver):
    '''
    获取年份
    :param driver:
    :return:
    '''
    links=driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/table/tbody/tr[4]/td[2]/span[position()>0]/a')

    # for item in links:
    #     print(item)
    #     print(item.text)

    return  links #返回的值包括链接和值



def pages(driver,loc):
    '''
    获取某一个年份的所有数据
    :param driver:
    :return:
    '''

    pages=driver.find_elements_by_xpath("/html/body/div[5]/div/div/div/a[position()>1]")
    pageParse(driver,loc)
    if pages==None:
        return
    try:
        while (pages[-1].text == u"下一页"):

            pages[-1].click()
            driver.implicitly_wait(10)
            pageParse(driver, loc)
            pages = driver.find_elements_by_xpath("/html/body/div[5]/div/div/div/a[position()>1]")

    except Exception,e:
        print("does't matter")
        return





def pageParse(driver,loc):
    '''
    parse the page and get the data
    :param driver:
    :return:
    '''

    #获取全部数据
    schoolNameLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[1]/a')
    stuTypeLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[2]')
    stuSrcLins=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[3]')
    caterLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[4]')
    yearLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[5]')
    rankLink=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[6]')
    highMarkLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[7]')
    lowMarkLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[8]')
    gradeRankLinks=driver.find_elements_by_xpath('/html/body/div[4]/div/div/table/tbody/tr[position()>1]/td[9]')



    length=len(schoolNameLinks)

    for count in range(length):
        name=schoolNameLinks[count].text
        stutype=stuTypeLinks[count].text
        stusrc=stuSrcLins[count].text
        cater=caterLinks[count].text
        year=yearLinks[count].text
        rank=rankLink[count].text
        highmark=highMarkLinks[count].text
        lowmark=lowMarkLinks[count].text
        graderank=gradeRankLinks[count].text

        save2db(name,stutype,stusrc,cater,year,rank,highmark,lowmark,graderank,loc)
        print(name, stutype, stusrc, cater, year, rank, highmark, lowmark, graderank,loc)
        #将数据导入数据库


def save2db(name,stutype,stusrc,cater,year,rank,highmark,lowmark,graderank,loc):
    '''
    将数据存入数据库
    :return:
    '''

    #连接到数据库
    db= MySQLdb.connect("localhost", "root", "lianglove3", "chiyuan", charset='utf8' )

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句

    sql="insert into enroll(collegename,stusrc,cater,stutype,rank,highmark,lowmark,graderank,year,area)\
        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
        %(name,stutype,stusrc,cater,rank,highmark,lowmark,graderank,year,loc)

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
    driver=login()
    catergory(driver)


