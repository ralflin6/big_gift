# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2022-05-04 12:34
# @Last Modified by:   oliver
# @Last Modified time: 2022-05-09 16:56
import os,re,zipfile
import sys
from django.shortcuts import redirect
from requests import session
from requests.utils import quote
import datetime
from hashlib import md5
from json import loads
import pandas as pd
from Logger import create_logger 
from argparse import ArgumentParser

logger = create_logger(os.path.join(os.path.dirname(os.path.abspath(__file__)),"worklog"), 'jiragetbug')

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
    
    headers = {}
    session_requests = session()
    result = session_requests.get(LOGIN_URL).text
    csrf_token = result[result.find('{"CSRF-Token": ')+16:result.find('{"CSRF-Token": ')+52]
    if '<html>' in csrf_token: #KX 不支援 csrf
        csrf_token = result[result.find("var csrf = '")+12:result.find("var csrf = '")+48]
        if '<html>' not in csrf_token:
            headers['csrf-token'] = csrf_token
        payload = {
            'name': NAME,
            'password': PASSWORD,
            'count': 0
        }
    if 'html' not in csrf_token:
        payload['_csrf'] = csrf_token
        headers['Cookie'] = f'_csrf={csrf_token}; '
    else:
        headers['Cookie'] = ''

    response = session_requests.request("POST", LOGIN_URL2, data=payload)
    
    try:
        csid = session_requests.cookies.get_dict()['connect.sid']
        headers['Cookie'] = headers['Cookie']  + 'lang=zh-CN;' f'connect.sid={csid}'
        fa = url+'/2fa/status'
        response = session_requests.post(fa, headers=headers)
    except:
        pass
    #確認是否登入成功
    try:
        result = session_requests.get(LOGIN_URL,headers=headers).text
        if '开发商后台' in result:  
            login_success = True
        else:
            raise Exception
    except Exception as e:
        print(str(e))
    
    alldata={}
    for account in list(acclist):
        limit=""
        for i in range(2):  
            payload ={
                "beginDate": begindate,
                "endDate": enddate,
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
    #確認要輸出的資料夾是否存在，不存在就建立
    if not os.path.isdir(export):
        os.mkdir(export)
    else:
        import shutil #如果原本存在就先移除，避免抓取到之前的資料
        shutil.rmtree(export)
        os.mkdir(export)
        
    for i in alldata:
        filtername=["CreateTime","Accounts","MoneyType","KindID","RoomType","TableID","ChairID","banker","TakeScore","AllBet","CellScore","Profit","Revenue","GameUserNO"]
        columnname=["账变时间","用户名","币种","游戏类型","房间类型","桌子号","座位号","庄闲","初始金额","总投注","有效投注额","盈利金额","抽水","局号"]
        alldata[i]=alldata[i][filtername]
        alldata[i].columns=columnname
        alldata[i].set_index("账变时间",inplace=True)
        alldata[i].to_excel(f'{export}/{i}.xlsx')
    #壓縮檔案 for jenkins upload
    zip_folder(export)

def getnamelist(file):
    a=pd.read_csv(file)
    return list(a)

def get_url_version(url):
    version_acc_pwd = {
        "KX" : {'acc' : 'guanli','pwd' : 'Abcd1234!'},
        "NW" : {'acc' : 'admin','pwd' : '123456a,'},
        "LY" : {'acc' : 'guanli','pwd' : 'Aa@123456'},
        "V8" : {'acc' : 'admin','pwd' : '123456a,'},
        "YL" : {'acc' : 'guanli','pwd' : '!Aa123456'}
    }
    session_requests = session()
    result = session_requests.get(url).text
    try:
        version_result = re.findall("favicon\/(.+)\/favicon",result)[0]
    except:
        version_result = "KX"
    for version_dict in list(version_acc_pwd): #回傳帳號密碼
        if version_dict.lower() in version_result.lower():
            return version_acc_pwd[version_dict]['acc'],version_acc_pwd[version_dict]['pwd']
        else:
            pass
    logger.error("無此版本帳密，請開發人員新增")

def zip_folder(local_dir): # 需壓縮的資料夾名稱
    try:
        zip_file_name = local_dir + '.zip'
        z = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(local_dir):
            fpath = dirpath.replace(local_dir,'')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath+filename)
                logger.debug('zip success')
        logger.info(''+ str(local_dir) +' zip success.')
        z.close()
        return True
    except Exception as e:
        logger.error(''+ str(local_dir) +' zip failed. '+ str(e) +'')
        return False


def parse_args():
    parser = ArgumentParser(prog='jiragetbug.py') 
    parser.add_argument('--backend_url', '-burl', default='', type=str, required=False, help='backend url')
    parser.add_argument('--account', '-acc', default='', type=str, required=False, help='account')
    parser.add_argument('--passward', '-pwd', default='', type=str, required=False, help='passward')
    parser.add_argument('--namelist', '-namelist', default='', type=str, required=False, help='namelist')
    parser.add_argument('--begindate', '-bdata', default='', type=str, required=False, help='begindate')
    parser.add_argument('--enddate', '-edata', default='', type=str, required=False, help='enddate')
    parser.add_argument('--file_path', '-file', default='', type=str, required=False, help='file path')
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args() #從外部取值
    url = args.backend_url

    acc = args.account
    pwd = args.passward
    if acc == '0':
        acc,pwd = get_url_version(url)
    else:
        pass

    namelist = args.namelist
    if ',' in namelist:
        namelist = namelist.split(',',)
    else:
        namelist = [namelist]

    begindate = args.begindate
    enddate = args.enddate
    if begindate == '0':
        begindate = ''
        enddate = ''
    else:
        pass
    file_path = './'+args.file_path
    getwinlosereport(url,acc,pwd,begindate,enddate,namelist,file_path)


