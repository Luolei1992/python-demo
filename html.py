#! /usr/bin/env python
# coding:utf-8

import urllib2
import threading
import bs4
import csv
import sys
# 防止中文乱码
reload(sys)
sys.setdefaultencoding('utf-8')

sec = 10
number = 90

# textarr = []     #电话
root_urls = 'http://m.1688.com'

# uri = "https://s.1688.com/company/company_search.htm?province=%D5%E3%BD%AD&n=y&pageSize=10&sortType=manufacture&biztype=1&offset=0&city=%C4%FE%B2%A8&filt=y&smToken=c1fa09b1448b4a88bb8ef26de8193bff&smSign=UW1HF13O51ylDzDbktQoMg%3D%3D&beginPage="
uri = "https://s.1688.com/company/company_search.htm?province=%D5%E3%BD%AD&n=y&pageSize=30&biztype=1&city=%C4%FE%B2%A8&filt=y&sortType=manufacture&offset=0&beginPage="

def hello(name):
    arrs = []     # 一页公司地址的集合
    global number
    global uri
    number += 1

   #  url = uri + number
    print number

    req = urllib2.Request(uri + str(number))
    req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
    file = urllib2.urlopen(req)
    html = file.read()
    arrs = get_video_page_urlf(html)
   #  print(gettelephone(gethref(arrs)))                    #得到数据
    outputcsv(gettelephone(gethref(arrs)))
    
    global timer
    timer = threading.Timer(sec, hello, ["Hawk"])
    timer.start()

if __name__ == "__main__":
    timer = threading.Timer(2, hello, ["Hawk"])
    timer.start()

def get_video_page_urlf(html):           #一页公司的地址
    soup = bs4.BeautifulSoup(html,'lxml')
    return soup.select('.list-item-title-text')

def gethref(arrs):
   array = []      # 移动端地址
   for arr in arrs:
      url = get_video_page_urls(arr.get('href'))
      array.append(url)
   return array

def get_video_page_urls(url):       #每个公司对应的移动端地址
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
    file = urllib2.urlopen(req)
    html = file.read()
    soup = bs4.BeautifulSoup(html,'lxml')
    return soup.select('meta[name^=mobile-agent]')[0].attrs['content'].split('winport')[1]
   #  return soup

def gettelephone(array):           #每个移动端地址获取电话
   # tep = {}
   textarr = []
   for uri in array:
      req = urllib2.Request(root_urls +'/winport/company'+ uri)
      req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
      file = urllib2.urlopen(req)
      html = file.read()
      soup = bs4.BeautifulSoup(html,'html.parser')
      # 公司名称
      infocompany = (soup.select('div.archive-baseInfo-companyInfo .info-container')[0].find('span').get_text())
      # 公司网址
      infopath = root_urls +'/winport'+ uri
      # 主营产品
      if len(soup.select('div.archive-baseInfo-companyInfo .info-container')) > 2:
         infoproduct = (soup.select('div.archive-baseInfo-companyInfo .info-container')[3].find('span').get_text())
      else:
         infoproduct = '0'
      # 经营模式
      # infotypes = (soup.select('div.archive-baseInfo-companyInfo .info-container')[1].find('span').get_text())
      # 联系人 联系地址
      infopersontmp = soup.select('div.archive-baseInfo-contactInfo .info-container')
      infoperson =  (infopersontmp[0].find('span').get_text() if (infopersontmp) else '0')
      # 判断是否有联系地址
      if len(soup.select('div.archive-baseInfo-contactInfo .info-container')) > 1 :
         infoaddress = soup.select('div.archive-baseInfo-contactInfo .info-container')[1].find('span').get_text()
      else:
         infoaddress = '0'
      # 电话
      infophonetmp = soup.select('div.phone')
      infophone = (infophonetmp[0].get_text() if (infophonetmp) else '0')
      # 在这里整理数据数据
      data = (
         # eval("'" + infocompany + "'")
         infocompany,
         infopath,
         infoproduct,
         # infotypes,
         infoperson,
         infoaddress,
         infophone
      )
      textarr.append(data)
   return textarr

def outputcsv(data):
   csvfile = open('csv1.csv', 'a+')  #打开方式还可以使用file对象,a+为数据添加
   writer = csv.writer(csvfile)
   # writer.writerow(['公司名称','公司网址','主营产品','联系人','联系地址','联系方式'])

   writer.writerows(data)

   csvfile.close()