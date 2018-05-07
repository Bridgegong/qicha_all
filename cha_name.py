# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 16:21
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : cha_name.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import requests
import pymysql
import time

class QiCha():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Cookie': 'UM_distinctid=162cd808014161-00492bb4fc9342-3a614f0b-100200-162cd808015360; zg_did=%7B%22did%22%3A%20%22162cd80809b7a3-00b9bdb2ca419-3a614f0b-100200-162cd80809c10f%22%7D; _uab_collina=152386617796255655450159; PHPSESSID=tjjd4q7pkmdefgrfd0th693730; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1524320429,1524320783,1524645514,1525338180; hasShow=1; acw_tc=AQAAADy69Q3pegoAHp9e01/bbo+bvHfD; _umdata=E2AE90FA4E0E42DE1797FE5A5EA7EC0A585D0DE88DAF395836028356558B6BD2BE235A35BC0930A0CD43AD3E795C914CA1D3A8786EE4A63655EF4160BDDC9D8D; CNZZDATA1254842228=886174903-1523864014-https%253A%252F%252Fwww.baidu.com%252F%7C1525340269; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525340276; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525340242697%2C%22updated%22%3A%201525340289606%2C%22info%22%3A%201525338179876%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%220b080986269b38bdff21c7f8ec855408%22%7D'}
        self.conn = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="zhiyin", use_unicode=True, charset="utf8")
        self.cur = self.conn.cursor()
        if self.cur:
            print("连接成功")
        else:
            print("连接失败")

    def get_url(self, url, name1):
        bea = self.get_requests(url)
        ur = bea.find_all('td')[1]
        self.get_page('http://www.qichacha.com' + ur.a['href'], ur.a['href'], name1)

    def get_page(self, urls, url_id, name1): # 去请求该链接有几页的对外投资
        print(urls)
        num = self.get_requests(urls)
        time.sleep(10)
        try:
            nums = num.find_all('span', 'tbadge')[1].text
            print(nums)
            page = divmod(int(nums), 10)
            if page[1] == 0:
                page = page[0]
            else:
                page = page[0] + 1
            for i in range(1, page + 1):
                print(i)
                self.get_con(url_id, i, urls, name1)
        except Exception as e:
            print(e)
            with open('D:\ZHiYin\qichacha\error.txt', 'a+',encoding='utf-8') as f:
                f.write('%s'%name1 + '\n')

    def get_con(self, url_id, num, urls, name1):
        id = url_id.split('_')[1].split('.')[0]
        url = 'http://www.qichacha.com/company_getinfos?unique={0}&companyname=%E5%9B%BD%E7%BD%91%E5%8C%97%E4%BA%AC%E5%B8%82%E7%94%B5%E5%8A%9B%E5%85%AC%E5%8F%B8&p={1}&tab=base&box=touzi'.format(id, num)
        print(url)
        bea = self.get_requests(url)
        time.sleep(6.6)
        name = bea.find_all('tr')[1:]
        for n in name:
            names = n.find_all('td')[0].text.replace(' ', '')
            name_user = n.find_all('td')[1].text.replace('对外投资与任职 >','').replace(' ', '')
            register_money = n.find_all('td')[2].text.replace('\n', '').replace('                      ', '')
            register_key = n.find_all('td')[3].text.replace('\n', '').replace('                      ', '').replace('  ','')
            data = n.find_all('td')[4].text.replace('\n', '').replace('                      ', '').replace(' ', '')
            status = n.find_all('td')[5].text.replace('\n', '').replace('                      ', '')
            print(urls)
            print(name1)
            print(names)
            sql = "insert into haihang_name(`Url`,FindName,`Names`,NameUser,RegisterAssets,Capitalkey,StartDate,Status,`Type`) VALUES ('%s','%s','%s','%s','%s','%s', '%s', '%s', '%s')" % (urls, name1, names, name_user, register_money, register_key, data, status, '4')
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)

    def get_requests(self, url):
        try:
            rep = requests.get('%s' % url, timeout=20, headers=self.header)
            rep.encoding = rep.apparent_encoding
            bea = BeautifulSoup(rep.text, 'lxml')
            return bea
        except Exception as e:
            print(e)

    def main(self):
        f = open(r'D:\ZHiYin\qichacha\names.txt')
        f.readline()
        for name in f:
            print(name)
            url = 'http://www.qichacha.com/search?key={}'.format(name)
            self.get_url(url, name)


if __name__ == '__main__':
    qi = QiCha().main()
