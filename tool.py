# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2021-07-13 16:38
# @Last Modified by:   oliver
# @Last Modified time: 2022-03-09 17:42
import os
#region 模組導入
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import datetime
import logging
loglocation=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir,"worklog",str(datetime.date.today())+"log.txt"))
logging.basicConfig(
    filename=loglocation,
    level=logging.INFO,
    format='%(asctime)s- %(filename)s-%(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


#endregion
'''
找餅乾
'''
def kxqa_guanli_cookies():
    '''
    KXQA管理後台cookies
    '''
    #管理後台帳號
    account='guanli'
    #管理後台密碼
    password='abc123!'
    #管理後台網址
    url='http://192.168.21.103:9100/default'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="MERCHANT_USERNAME"]').send_keys(account)
    driver.find_element_by_xpath('//*[@id="MERCHANT_PWD"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="login"]').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies
def kxqa_song_cookies():
    '''
    KX爽哥cookies
    '''
    #爽哥帳號
    account='admin'
    #爽哥密碼
    password='abc123!'
    #爽哥網址
    url='http://192.168.21.119:7070/login'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/input[1]').send_keys(account)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/input[2]').send_keys(password)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/button').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies
def kxcb_guanli_cookies():
    '''
    KXCB管理後台cookies
    '''
    #管理後台帳號
    account='guanli'
    #管理後台密碼
    password='abc123!'
    #管理後台網址
    url='https://nc1-ht.twow42.com/default'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="MERCHANT_USERNAME"]').send_keys(account)
    driver.find_element_by_xpath('//*[@id="MERCHANT_PWD"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="login"]').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies
def kxcb_song_cookies():
    '''
    KX爽哥cookies
    '''
    #爽哥帳號
    account='admin'
    #爽哥密碼
    password='abc123!'
    #爽哥網址
    url='https://nc1-song.twow42.com/login'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/input[1]').send_keys(account)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/input[2]').send_keys(password)
    driver.find_element_by_xpath('/html/body/div/div/div/div/form/button').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies
def nwqa_guanli_cookies():
    '''
    NWQA管理後台cookies
    '''
    #管理後台帳號
    account='admin'
    #管理後台密碼
    password='123456a,'
    #管理後台網址
    url='http://192.168.22.113:9100/default'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[1]/div/input').send_keys(account)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[2]/div/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[5]/button').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies
def nwcb_guanli_cookies():
    '''
    NWCB管理後台cookies
    '''
    #管理後台帳號
    account='admin'
    #管理後台密碼
    password='123456'
    #管理後台網址
    url='https://nc1-ht.dlmd40.com/default'
    #撈cookie
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[1]/div/input').send_keys(account)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[2]/div/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginContent"]/div[2]/div[5]/button').click()
    driver.refresh()
    c = driver.get_cookies()
    driver.close()
    cookies = {}
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    return cookies



def findallmember(proxy,server):
    '''
    輸入代理 ex:60186
    輸入SERVER ex: KXQA,KXCB

    找其代理及子代理所有底下會員
    '''
    #設定server資訊
    if server=='KXQA':
        guanli_cookies=kxqa_guanli_cookies()
        guanli_api='http://192.168.21.103:9100/'
    if server=='KXCB':
        guanli_cookies=kxcb_guanli_cookies()
        guanli_api='https://nc1-ht.twow42.com/'
    if server=='NWQA':
        guanli_cookies=nwqa_guanli_cookies()
        guanli_api='http://192.168.22.113:9100/'
    if server=='NWCB':
        guanli_cookies=nwcb_guanli_cookies()
        guanli_api='https://nc1-ht.dlmd40.com/'

    search_proxy=[proxy]
    member=[]
    #打接口取得子代理
    search_proxy=[proxy]
    r=requests.get(guanli_api+'proxyaccount/GetList?limit=214748364&offset=0&Accounts=&proxyUID='+str(proxy)+'&proxyUIDS=&NickName=&ChannelID=',cookies=guanli_cookies)
    for i in range(len(r.json()['rows'])):
        search_proxy.append(r.json()['rows'][i]['ChannelID'])
    print('search_proxy:',search_proxy)
    #取得所有帳號
    for i in range(len(search_proxy)):
        r=requests.get(guanli_api+'memberinfo/GetList?limit=2147483647&offset=0&Accounts=&total=0&selstatus=-1&Proxyaccount='+str(search_proxy[i])+'&hidserch=1&_=1625820384835',cookies=guanli_cookies)
        for j in range(len(r.json()['rows'])):
            member.append(r.json()['rows'][j]['name'])
    print('member:',member)
    
    return member

def addproxy(proxy_name,server):
    '''
    輸入代理名稱 ex: AgentApple
    輸入SERVER ex: KXQA,KXCB

    新增代理至可登入(爽哥)
    '''
    #設定server資訊
    if server=='KXQA':
        guanli_cookies=kxqa_guanli_cookies()
        song_cookies=kxqa_song_cookies()
        guanli_api='http://192.168.21.103:9100/'
        song_api='http://192.168.21.119:7070/'
    if server=='KXCB':
        guanli_cookies=kxcb_guanli_cookies()
        song_cookies=kxcb_song_cookies()
        guanli_api='https://nc1-ht.twow42.com/'
        song_api='https://nc1-song.twow42.com/'        
        
    #新增代理
    my_data = {
                'id': '',
                'sel_MoneyType': '1',
                'ProxyAccount': proxy_name,
                'ProxyPawd': 'dbb342c8604b24b466a1920002a14858',
                'NickName': '',
                'AccountingFor': '100',
                'WhiteIP': '',
                'Mark': '',
                'CallBackURL': '0',
                'ProxyURL': '',
                'Forbidden': '0',
                'ProxyRevenue': '',
                'Pushbutton': '0',
                'Deskey': '',
                'Md5key': '',
                'banckstatus': '0',
                'CallBackLink':  '',
                'feedEnabled': '0',
                'Cooperation': '0',
                'Timezone': '0',
                'Winloschart': '1',
                'Disablelinecode': '0',
                'logourl':  '',
                'automatch': '1',
                'skins': '',
                'defaultSkin[]': '1',
                'sbStatus': '0',
                'sbUrl':  '',
                'BusinessAccount': '',
                'DisBusinessAccount': '1',
                'SingleOrSystem': '0',
                'reseller': '',
                'JackpotSupport': '0',
                'JackpotNotice': '0',
                'JackpotAllowGrand': '0',
               }
    
    r = requests.post(guanli_api+'proxyaccount/addProxy',data=my_data,cookies=guanli_cookies)
    
    #取得代理id
    r = requests.get(guanli_api+'proxyaccount/GetList?limit=2147483647&offset=0&Accounts=&proxyUID=&proxyUIDS=&NickName=&ChannelID=&order=asc', cookies=guanli_cookies)
    for i in range(len(r.json()['rows'])):
        if r.json()['rows'][i]['Accounts']==proxy_name:
            ChannelID=r.json()['rows'][i]['ChannelID']
    
    #代理加白名單
    my_data={
        'ChannelID':ChannelID,
        'WhiteIP':'192.168.20.205,59.188.84.60,59.188.78.89,127.0.0.1',
        'WhiteIPInherit':'0'
        }
    r = requests.post(guanli_api+'proxyaccount/updateApiWhiteList',data=my_data,cookies=guanli_cookies)
    #取得代理秘鑰
    my_data={'ChannelID':ChannelID}
    r = requests.post(guanli_api+'proxyaccount/getproxybyid',data=my_data,cookies=guanli_cookies)
    Deskey=r.json()['dataproxy'][0]['Deskey']
    Md5key=r.json()['dataproxy'][0]['Md5key']
    
    #新增爽哥入口
    my_data={
        'serverCode': 'cn-test',
        'agent': ChannelID,
        'desKey': Deskey,
        'md5Key': Md5key,
    }
    r= requests.post(song_api+'setting/agent/save',data=my_data,cookies=song_cookies)

findallmember(89,"NWCB")