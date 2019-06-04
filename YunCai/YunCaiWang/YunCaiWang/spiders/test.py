# -*- coding:utf-8 -*- 
# author:Px

import requests
import lxml
def getcookie(cookie):
    item_dict = {}
    for item in cookie.split(';'):
        item_dict[item.split('=')[0].strip()] = item.split('=')[1].strip()
    print item_dict


def deletehtml():
    from bs4 import BeautifulSoup
    with open('C:/Users/Administrator/Desktop/1.html','r+')as f:
        html = f.read().decode('gbk')
        con = BeautifulSoup(html).find_all('div',class_="col-md-9 left")[0]
        div = con.find_all('div',class_="form-group form-group-btn text-center")[0]
        blockquote = con.find_all('blockquote')[0]
        blockquote.clear()
        div.clear()

        print con
        # html_obj = BeautifulSoup(html)
        # con = BeautifulSoup(str(BeautifulSoup(html_obj).find_all('div',class_="col-md-9 left")[0]))
        #
        # div = con.find_all('div',class_="form-group form-group-btn text-center")[0]
        # div.clear()
        # print con




if __name__ =='__main__':
    # getcookie('UM_distinctid=167dfc027745b2-0fccd331595a7f-39614101-1fa400-167dfc027752ff; ASP.NET_SessionId=4rqdxjabcoq2j530nv1f2omk; CNZZDATA1256138383=354838283-1545645874-null%7C1545699106')
    deletehtml()