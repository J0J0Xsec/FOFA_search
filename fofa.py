import requests
import os
import sys
from lxml import etree
import base64
import re
import time
import base
import config
from urllib.parse import quote,unquote
def banner():
    print("\033[1;32m-------------------------------------------------------------------基于cookie的普通版（游客和会员都能用）-----------------------------------------------------------\033[0m")
def spider():
    timesleep=input('请输入等待时间（建议3秒）>>>\n')
    if str(timesleep) == "exit":
        sys.exit(0)
    else:
       search_content=input('请输入FOFA语法>>>\n')
    if search_content == "exit":
        sys.exit(0)
    else:
        search_bs64 = str(base64.b64encode(search_content.encode('utf-8')), 'utf-8')
        fofa_token=input('登录FOFA后的token >>>\n')
    if fofa_token == "exit":
        sys.exit(0)
    else:
        header={
            "Connection": "keep-alive",
            "Authorization": fofa_token
           }
    print("爬取页面为:https://fofa.so/result?qbase64=" + search_bs64)
    html = requests.get(url="https://fofa.so/result?qbase64=" + search_bs64,headers=header).text
    tree = etree.HTML(html)
    pagenum=tree.xpath('//li[@class="number"]/text()')[-1]
    print("该关键字存在页码: >>>"+str(pagenum))
    StartPage=input("请输入开始页码: >>>\n")
    StopPage=input("请输入结束页码: >>>\n")
    pagenumber=int(pagenum)+1
    urldata = open("urldata.txt", "a+")
    for i in range((int(StartPage)),pagenumber):
        print("WAIT.... " + str(i) + " page")
        rep = requests.get('https://api.fofa.so/v1/search?qbase64=' + search_bs64+"&full=false&pn="+str(i)+"&ps=10", headers=header)
        pattern = re.compile('"link":"(.*?)",')
        urllist = re.findall(pattern, rep.text)
        print(urllist)
        for j in urllist:
            print(j)
            urldata.write(j+"\n")
        if i==int(StopPage):
            break
        time.sleep(int(timesleep))
    urldata.close()
    print("OK .")


def main():
    banner()
    base.logo()
    spider()

if __name__ == '__main__':
    main()
