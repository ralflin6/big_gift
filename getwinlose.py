# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2022-05-04 12:34
# @Last Modified by:   oliver
# @Last Modified time: 2022-05-09 16:56
import os
import sys
from django.shortcuts import redirect
from requests import session
from requests.utils import quote
import datetime
from hashlib import md5
from json import loads
import pandas as pd
import logging
loglocation=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir,"worklog",str(datetime.date.today())+"log.txt"))
logging.basicConfig(
    filename=loglocation,
    level=logging.INFO,
    format='%(asctime)s- %(filename)s-%(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def getwinlosereport(homepage,acc,pwd,begindate,enddate,acclist,export):
    try:
        url = str(homepage).replace('default?language=cn','').replace('default','').strip('/')
    except KeyError:
        print("尚未添加後台資料，請至setup添加")
        os.system('pause')
        sys.exit()
        
    NAME = acc
    PASSWORD = md5(str(pwd).encode("utf-8")).hexdigest()
    LOGIN_URL = url+'/default'
    LOGIN_URL2 = url+'/login'
    
    session_requests = session()
    result = session_requests.get(LOGIN_URL).text
    csrf_token = result[result.find('{"CSRF-Token": ')+16:result.find('{"CSRF-Token": ')+52]
    if '<html>' in csrf_token:
        csrf_token = result[result.find(
            "var csrf = '")+12:result.find("var csrf = '")+48]
    headers = {
        'csrf-token': csrf_token
    }
    payload = {
        'name': NAME,
        'password': PASSWORD,
        'count': 0
    }


    if 'html' not in csrf_token:
        payload = {
        'name': NAME,
        'password': PASSWORD,
        'count': 0,
        '_csrf':csrf_token
        }
        response = session_requests.request("POST", LOGIN_URL2, data=payload)
    else:
        response = session_requests.request("POST", LOGIN_URL2, data=payload)
    try:
        csid = result.cookies.get_dict()['connect.sid']
        headers = {
            'Cookie': 'lang=zh-CN;' f'connect.sid={csid}'
        }
        fa = url+'/2fa/status'
        response = session_requests.post(fa, headers=headers)
    except:
        pass
    
    alldata={}
    for account in list(acclist):
        limit=""
        for i in range(2):  
            payload ={
                "beginDate": quote(begindate),
                "endDate": quote(enddate),
                "kindId":"" ,
                "accounts": account,
                "serverId": "",
                "limit": limit,
                "offset": "0",
                "total": "0",
                "GameUserNO": "",
                "moneyType": 0,
                "productID": 2,
                "_": 1651729767135,
            }
            response = session_requests.request("GET", url+'/winAndLoseReport/InitData', params=payload)
            data=loads(response.content)
            limit=data["total"]
            alldata[account]=pd.DataFrame(data["rows"])

    for i in alldata:
        filtername=["CreateTime","Accounts","MoneyType","KindID","RoomType","TableID","ChairID","banker","TakeScore","AllBet","CellScore","Profit","Revenue","GameUserNO"]
        columnname=["账变时间","用户名","币种","游戏类型","房间类型","桌子号","座位号","庄闲","初始金额","总投注","有效投注额","盈利金额","抽水","局号"]
        alldata[i]=alldata[i][filtername]
        alldata[i].columns=columnname
        alldata[i].set_index("账变时间",inplace=True)
        alldata[i].to_excel(f'{export}/{i}.xlsx')

def getnamelist(file):
    a=pd.read_csv(file)
    return list(a)





if __name__ == "__main__":
    url="http://192.168.12.91:9100/default"
    acc="admin"
    pwd="123456a,"
    begindate="2022-05-05+00:00:00"
    enddate="2022-05-10+00:00:00"

    getwinlosereport(url,acc,pwd,begindate,enddate,getnamelist("C:/Users/oliverchiu/Desktop/namelist.txt"),"C:/Users/oliverchiu/Desktop/packing/data")


