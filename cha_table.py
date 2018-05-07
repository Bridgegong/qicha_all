# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 15:38
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : cha_table.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import requests
import pymysql
import time


class QiCha():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Cookie': 'PHPSESSID=me22q2i8vo970aha7m002m0uh3; UM_distinctid=162cd808014161-00492bb4fc9342-3a614f0b-100200-162cd808015360; CNZZDATA1254842228=886174903-1523864014-https%253A%252F%252Fwww.baidu.com%252F%7C1523864014; zg_did=%7B%22did%22%3A%20%22162cd80809b7a3-00b9bdb2ca419-3a614f0b-100200-162cd80809c10f%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1523866174; hasShow=1; acw_tc=AQAAAIB0pWtZrQ4AHp9e04FzP/GsTMyp; _uab_collina=152386617796255655450159; _umdata=E2AE90FA4E0E42DE1797FE5A5EA7EC0A585D0DE88DAF395836028356558B6BD2BE235A35BC0930A0CD43AD3E795C914CD792973041077B79DEADE910A284691D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1523867445; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201523866173601%2C%22updated%22%3A%201523867444856%2C%22info%22%3A%201523866173604%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%220b080986269b38bdff21c7f8ec855408%22%7D'
        }
        self.conn = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="zhiyin", use_unicode=True, charset="utf8")
        self.cur = self.conn.cursor()
        if self.cur:
            print("连接成功")
        else:
            print("连接失败")

    def get_url(self, url, name):
        bea = self.get_requests(url)
        time.sleep(3.6)
        try:
            ur = bea.find_all('td')[1]
            self.get_con('http://www.qichacha.com' + ur.a['href'], name)
        except Exception as e:
            print(e)
            # with open('D:\ZHiYin\qichacha\error_table.txt', 'a+', encoding='utf-8') as f:
            #     f.write('%s'%name + '\n')

    def get_con(self, urls, name_main):
        print(urls)
        bea = self.get_requests(urls)
        try:
            na = bea.find_all('div', 'pull-left')[1]
            name_user = na.find('a', 'bname').text # 法定代表人信息
        except Exception as e:
            print(e)
            with open('D:\ZHiYin\qichacha\error_table.txt', 'a+', encoding='utf-8') as f:
                f.write('%s'%name_main + '\n')
        try:
            table_all = bea.find_all('table', 'ntable')[1]
            table_list = table_all.find_all('td')
            # 注册资本
            register_money = table_list[1].text.replace('\n','').replace('                 ','')
            print(register_money)
            # 实缴资本
            true_money = table_list[3].text.replace('\n','').replace('                ','')
            print(true_money)
            # 经营状态
            status = table_list[5].text.replace('\n','').replace('                 ','')
            print(status)
            # 成立日期
            start_data = table_list[7].text.replace('\n','').replace('                ','')
            print(start_data)
            # 注册号
            register_id = table_list[9].text.replace('\n','').replace('                ','')
            print(register_id)
            # 组织机构代码
            tissue_code = table_list[11].text.replace('\n','').replace('                ','')
            print(tissue_code)
            # 纳税人识别号
            user_num = table_list[13].text.replace('\n', '').replace('                ', '')
            print(user_num)
            # 统一社会信用代码
            credit_code = table_list[15].text.replace('\n', '').replace('                ', '')
            print(credit_code)
            # 公司类型
            company_type = table_list[17].text.replace('\n', '').replace('  ', '')
            print(company_type)
            # 所属行业
            industry_involved = table_list[19].text.replace('\n', '').replace('  ', '')
            print(industry_involved)
            # 核准日期
            approve_data = table_list[21].text.replace('\n', '').replace('              ', '')
            print(approve_data)
            # 登记机关
            register_office = table_list[23].text.replace('\n', '').replace('              ', '')
            print(register_office)
            # 所属地区
            affiliating_area = table_list[25].text.replace('\n', '').replace('                ', '')
            print(affiliating_area)
            # 英文名
            english_name = table_list[27].text.replace('\n', '').replace('                ', '')
            print(english_name)
            # 曾用名
            used_name = table_list[29].text.replace('\n', '').replace('                ', '')
            print(used_name)
            # 经营方式
            business_pattern = table_list[31].text.replace('\n', '').replace('                ', '')
            print(business_pattern)
            # 人员规模
            user_size = table_list[33].text.replace('\n', '').replace('                ', '')
            print(user_size)
            # 营业期限
            business_term = table_list[35].text.replace('\n', '').replace('                ', '')
            print(business_term)
            # 企业地址
            adders = table_list[37].text.replace('\n', '').replace('查看地图  附近公司', '').replace('                 ','')
            print(adders)
            # 经营范围
            run_range = table_list[39].text.replace('\n', '').replace('                ', '')
            print(run_range)
            # 法律诉讼
            lawsuit = bea.find_all('div','company-nav-tab')[1].span.text.replace('+','')
            print(lawsuit)
            # 知识产权
            property = bea.find_all('div','company-nav-tab')[5].span.text.replace('+','')
            print(property)
            sql = "insert into qicha_con(`Url`,`Name`,Name_user,Register_money,True_money,Status,Start_data,Register_id,Tissue_code,User_num,Credit_code,Industry_involved,Company_type,Approve_data,Register_office,Affiliating_area,English_name,Used_name,Business_pattern,User_size,Business_term,Adders,Run_range,Lawsuit,Property) VALUES ('%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s', '%s', '%s','%d','%d' )" % (
            urls,name_main,name_user,register_money,true_money,status,start_data,register_id,tissue_code,user_num,credit_code,industry_involved,company_type,approve_data,register_office,affiliating_area,'english_name',used_name,business_pattern,user_size,business_term,adders,run_range,int(lawsuit),int(property))
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                with open('D:\ZHiYin\qichacha\error_table.txt', 'a+', encoding='utf-8') as f:
                    f.write('%s'%name_main + '\n')
        except Exception as e:
            print(e)
            # with open('D:\ZHiYin\qichacha\error_table.txt', 'a+', encoding='utf-8') as f:
            #     f.write('%s' % name_user + '\n')

    def get_requests(self, url):
        try:
            rep = requests.get('%s' % url, timeout=20, headers=self.header)
            rep.encoding = rep.apparent_encoding
            bea = BeautifulSoup(rep.text, 'lxml')
            return bea
        except Exception as e:
            print(e)


    def main(self):
        f = open(r'D:\ZHiYin\qichacha\name_con.txt')
        f.readline()
        for name in f:
            print(name)
            time.sleep(6.6)
            url = 'http://www.qichacha.com/search?key={}'.format(name)
            self.get_url(url, name)


if __name__ == '__main__':
    qi = QiCha().main()
