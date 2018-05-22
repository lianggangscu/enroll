#!/usr/bin/env python
#encoding:utf-8

from selenium import webdriver
import pickle
import time
import  MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')


url='https://www.cdzk.cn'
usrname="13688329270" #science
#usrname="13518151051" #art
passwd="lwy0318"




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

def getTask(filename="science.txt"):

    '''
    获取任务
    :param filename:
    :return:
    '''
    with open(filename) as f:
        tasks=pickle.load(f)


    # for item in tasks:
    #     print(item)

    return tasks

def getData(bro,task):
    '''

    对每个任务进行解析
    get the real data and save to db
    :param tasks:
    :return:
    '''


    #首先获取任务url的地址
    finurl=url+task[0]
    # print(task)

    #other 存放学校名字，文理，录取批次，省份
    other=task[1:]
    # print(other)
    # print(finurl)


    #进入到专业页面
    bro.get(finurl)
    bro.implicitly_wait(10)

    #获得学校的基本信息,学校数据的爬取建议和专业数据的爬取分开，一个是速度的原因，一个是避免错误的问题
    #parseCollege(bro,finurl,other)
    #获得学校的专业信息
    protask=parsePro(bro,finurl)

    return protask



def parsePro(bro,url):
    '''
    解析页面专业分数
    :param bro:
    :return:
    '''

    #获得每一个学校所有专业信息列表
    protasks=[]




    #需要确定专业页面次数的问题,同时也可以判断页面是否存在元素
    pages=bro.find_elements_by_xpath('//*[@id="pager"]/ul/li')
    length=len(pages)
    if length==13:
        bro.find_element_by_xpath('//*[@id="pager"]/ul/li[13]').click()
        bro.implicitly_wait(10)

        temp=bro.find_element_by_xpath('//*[@id="pager"]/ul/li[11]')
        length=int(temp.text)+4

        #back to the first page
        bro.get(url)
        bro.implicitly_wait(10)



    count=length-4

    if(count==0):
        return

    while(count>0):
        count-=1

        #获得专业名字
        try:
            proNames=bro.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[position()>0]/td[1]/a')

        except Exception,e:
            proNames = bro.find_elements_by_xpath('//*[@id="tadatalist"]/tr[position()>0]/td[1]/a')


        leng=len(proNames)

        #除了最后一页，每页有10个专业
        print(leng)

        for item in range(leng):
            #获得每个专业的数据
            proPage=proNames[item].get_attribute("href")
            print(proPage)
            protasks.append(proNames[item].get_attribute("href"))
            #获取每一个专业的的专业分数
            #bro=parseProPage(bro,proPage)







        #如果不是最后一页就翻页
        if (count!=0):
            bro.find_elements_by_xpath('//*[@id="pager"]/ul/li')[-2].click()
            bro.implicitly_wait(10)

    return protasks

def parseProPage(bro,herf):
    '''
    获取每个专业的基本数据
    :param bro:
    :param herf:
    :return:
    '''

    #跳转到具体的具体的某一个专业页面

    bro.get(herf)
    bro.implicitly_wait(10)



    bro.back()
    bro.implicitly_wait(10)
    return bro








def parseCollege(bro,url,other):


    type=0 #type=0 表示本科，为1表示专科
    # jump to the college page
    bro.get(url)
    bro.implicitly_wait(10)



    bro.find_element_by_xpath('/html/body/ul/li[2]/a').click()
    bro.implicitly_wait(10)


    #需要对本科和专科的页面进行区分

    types=bro.find_elements_by_xpath('/html/body/table/tbody/tr/th/a')
    leng=len(types)

    #getdata from the page
    if(leng!=4):
        try:
            years = bro.find_elements_by_xpath('/html/body/table/thead/tr/th[position()>1]')
            scores = bro.find_elements_by_xpath('/html/body/table/tbody/tr[1]/td[position()>0]')
            aveScores = bro.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[position()>0]')
            diff = bro.find_elements_by_xpath('/html/body/table/tbody/tr[3]/td[position()>0]')
            averdiff = bro.find_elements_by_xpath('/html/body/table/tbody/tr[4]/td[position()>0]')
            rank = bro.find_elements_by_xpath('/html/body/table/tbody/tr[5]/td[position()>0]')
            averank = bro.find_elements_by_xpath('/html/body/table/tbody/tr[6]/td[position()>0]')
        except Exception:
            return
    else:
        try:
            years = bro.find_elements_by_xpath('/html/body/table/thead/tr/th[position()>1]')
            scores = bro.find_elements_by_xpath('/html/body/table/tbody/tr[1]/td[position()>0]')
            aveScores = bro.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[position()>0]')
            diff = bro.find_elements_by_xpath('/html/body/table/tbody/tr[3]/td[position()>0]')
            averdiff = bro.find_elements_by_xpath('/html/body/table/tbody/tr[4]/td[position()>0]')
            rank=[0*item for item in range(len(years))]
            averank=[0*item for item in range(len(years))]
            type=1
        except Exception:
            return


    length = len(years)
    for item in range(length):
        if (leng!=4):
            try:
                collegename=other[0]
                pro=other[-1]
                cater=other[1]
                enterorder=other[2]
                saveCollege(collegename,pro,cater,enterorder,years[item].text, scores[item].text, aveScores[item].text, diff[item].text, averdiff[item].text, rank[item].text, averank[item].text)
                print(collegename, pro, cater, enterorder, years[item].text, scores[item].text, aveScores[item].text,
                            diff[item].text, averdiff[item].text, rank[item].text, averank[item].text)
            except Exception:
                return
        else:
            try:
                print(collegename, pro, cater, enterorder, years[item].text, scores[item].text, aveScores[item].text,
                            diff[item].text, averdiff[item].text,
                            rank[item], averank[item])
                saveCollege(collegename,pro,cater,enterorder,years[item].text, scores[item].text, aveScores[item].text, diff[item].text, averdiff[item].text,
                      rank[item], averank[item])
            except:
                return

def saveCollege(collegename, pro, cater, enterorder, year, score, avescore, diff, avediff, rank, averank):
        '''
        将数据存入数据库
        :return:
        '''

        # 连接到数据库
        db = MySQLdb.connect("localhost", "root", "lianglove3", "chiyuan", charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "insert into college(collegename,province,cater,enterorder,year,score,aver,diff,averdiff,rank,averrank)\
              values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
              % (collegename, pro, cater, enterorder, year, score, avescore, diff, avediff, rank, averank)

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception, e:
            # 发生错误时回滚
            print(e)
            db.rollback()

        # 关闭数据库连接
        db.close()


def savePro():
    pass

if __name__=="__main__":

    #get the tasklists
    tasks=getTask()

    #login to the website ，因为下载网页必须要登陆
    protasks=[]
    bro=simLogin()
    for task in tasks:
        protask=getData(bro,task)
        if protask!=None:
            print(protask)
            protasks.extend(protask)

    with open("sciencepro.txt","w") as f:
        pickle.dump(protasks,f)





