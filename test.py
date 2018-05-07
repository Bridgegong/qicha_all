# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 0020 上午 11:21
# @Author  : LiuLei
# @Email   : liulei@knowlegene.com
# @File    : invest_touzitupu.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import datetime
import pymysql
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import json
import pymysql
from selenium.webdriver.common.by import By
import re

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
         'Cookie':'_uab_collina=150095302219345786354525; gr_user_id=3558dff4-bf8d-422e-bfd9-dc19ac9b8287; UM_distinctid=161269ca5f229a-08d2428e26d5a7-5c1b3517-100200-161269ca5f57e8; zg_did=%7B%22did%22%3A%20%2215f15cfeea3c7-089e04c841bad-5c1b3517-100200-15f15cfeea4603%22%7D; PHPSESSID=hhr1534md6ibec8nkbeom5dot3; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1523349818,1523597605,1524126437,1524193549; hasShow=1; acw_tc=AQAAAIQo3Q5vFQMAHp9e0+a4/jE6bk9V; _umdata=BA335E4DD2FD504FF07484DA9D5BA2DBB1C818530BAE616C852AAC60EC198B787FCF261779477419CD43AD3E795C914C8A2D813F6BEAAE5D941849B5DBE97F7C; CNZZDATA1254842228=880884596-1500949657-https%253A%252F%252Fwww.baidu.com%252F%7C1524201263; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201524201740504%2C%22updated%22%3A%201524204895214%2C%22info%22%3A%201524126436147%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%226f3d82aff6de16ea089532a9d899c047%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1524204896'
         }
gdlist = []
tzlist = []
def get_key(comName):
    url="http://www.qichacha.com/search?key="+comName
    searchsoup=requests.get(url,headers=headers,timeout=20).content
    time.sleep(10)
    searchsoup=BeautifulSoup(searchsoup,'lxml')
    fircom=searchsoup.find('table',{'class':'m_srchList'}).find('tbody').find_all('tr')[0]
    keyno1=fircom.find('td').find('img').get('src')

    keyno=keyno1.split('/')[-1]
    keyno=keyno.strip(".jpg")
    print(keyno)

    return keyno


########得到所有的投资

def get_TZchildren(id,name,ss):

    if(ss['children']==None):

            tid = ss['KeyNo']
            tname = ss['name']
            fname = name
            fid=id
            FundedAmount = ss['FundedAmount']
            FundedRate = ss['FundedRate']

            print("@@@@@@@@@@")
            print("投资" + "FromId：" + str(fid) + "----" + "ToId: " + str(tid))
            print("投资" + "Fname=" + str(fname) + "-----" + "TName=" + str(tname))
            print("@@@@@@@@@@")

            data={'fid':fid,'fname':fname,'tid':tid,'tname':tname,'fundedAmount':FundedAmount,'fundedRate':FundedRate}
            # list.append(data)
    else:

            for i in ss['children']:
                tid=i['KeyNo']
                fid=id
                fname=name
                tname=i['name']

                FundedAmount=i['FundedAmount']
                FundedRate=i['FundedRate']
                print("@@@@@@@@@@")
                print("投资"+"FromId："+str(fid)+"----"+"ToId: "+str(tid))
                print("投资"+"Fname="+str(fname)+"-----"+"TName="+str(tname))
                print("@@@@@@@@@@")
                data = {'fid':fid,'fname':fname,'tid':tid,'tname':tname,'fundedAmount':FundedAmount,'fundedRate':FundedRate}
                tzlist.append(data)

                get_TZchildren(tid,tname,i)

def get_GDchildren(id, name, ss):
    if (ss['children'] == None):

        fid = ss['KeyNo']
        fname = ss['name']
        tname = name
        tid = id
        FundedAmount = ss['FundedAmount']
        FundedRate = ss['FundedRate']
        print("判断了值是否为空")
        print("@@@@@@@@@@")
        print("股东" + "FromId：" + str(fid) + "----" + "ToId: " + str(tid))
        print("股东" + "Fname=" + str(fname) + "-----" + "TName=" + str(tname))
        print("@@@@@@@@@@")

        data = {'fid': fid, 'fname': fname, 'tid': tid, 'tname': tname, 'fundedAmount': FundedAmount,
                'fundedRate': FundedRate}
        # # list.append(data)
    else:

        for i in ss['children']:
            fid = i['KeyNo']
            tid = id
            tname = name
            fname = i['name']

            FundedAmount = i['FundedAmount']
            FundedRate = i['FundedRate']
            print("@@@@@@@@@@")
            print("股东" + "FromId：" + str(fid) + "----" + "ToId: " + str(tid))
            print("股东" + "Fname=" + str(fname) + "-----" + "TName=" + str(tname))
            print("@@@@@@@@@@")
            data = {'fid': fid, 'fname': fname, 'tid': tid, 'tname': tname, 'fundedAmount': FundedAmount,
                    'fundedRate': FundedRate}
            gdlist.append(data)

            get_GDchildren(fid, fname, i)
def get_json(keyno):

    #######投资图谱
    url='http://www.qichacha.com/cms_map?keyNo=%s&upstreamCount=4&downstreamCount=4'%(keyno)
    print(url)
    response = requests.get(url,headers=headers,timeout=20).text
    jsondes=response.encode('utf-8').decode('unicode_escape')
    # print(jsondes)

    js = json.loads(jsondes)

    #####第一层 公司的名字，keyno
    comName=js['Result']['Node']['name']
    keyno=js['Result']['Node']['KeyNo']

    print(comName)
    # print(keyno)
    ##########得到所有的股东



    ########股东
    for i in js['Result']['Node']['children'][0]['children']:


        ###第一层股东的信息
        fid=i['KeyNo']
        fname=i['name']
        FundedAmount = i['FundedAmount']
        FundedRate = i['FundedRate']
        tid=keyno
        tname=comName
        print("@@@@@@@@@@")
        print("股东" + "FromId：" + str(fid) + "----" + "ToId: " + str(tid))
        print("股东" + "Fname=" + str(fname) + "-----" + "TName=" + str(tname))
        print("@@@@@@@@@@")

        data = {'fid':fid,'fname':fname,'tid':tid,'tname':tname,'fundedAmount':FundedAmount,'fundedRate':FundedRate}
        gdlist.append(data)
        print(type(i))

        get_GDchildren(fid, fname, i)
    print(gdlist)
    with open("a.txt", 'a', encoding='utf-8') as a:
        a.write(str(gdlist))
        a.write('\n')
        gdlist.clear()


    ########投资关系
    for i in js['Result']['Node']['children'][1]['children']:
        ###第一层投资的信息
        tid = i['KeyNo']
        tname = i['name']
        FundedAmount = i['FundedAmount']
        FundedRate = i['FundedRate']
        fid = keyno
        fname = comName
        print("@@@@@@@@@@")
        print("投资" + "FromId：" + str(fid) + "----" + "ToId: " + str(tid))
        print("投资" + "Fname=" + str(fname) + "-----" + "TName=" + str(tname))
        print("@@@@@@@@@@")

        data = {'fid': fid, 'fname': fname, 'tid': tid, 'tname': tname, 'fundedAmount': FundedAmount,'fundedRate': FundedRate}
        tzlist.append(data)
        print(type(i))

        get_TZchildren(tid, tname, i)
    print(tzlist)

    with open("b.txt", 'a', encoding='utf-8') as b:
        b.write(str(tzlist))
        b.write('\n')
        tzlist.clear()



with open(r'D:\ZHiYin\qichacha\aguplus500.txt','r',encoding='utf-8') as l:
    for name in l:
        try:
            keyno=get_key(name)
            get_json(keyno)
        except(Exception )as a:
            print(a)



