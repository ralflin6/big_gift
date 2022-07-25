# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2021-10-29 14:07
# @Last Modified by:   oliver
# @Last Modified time: 2022-03-09 16:24
import os
from jira import JIRA
import pandas as pd
import datetime
from Logger import create_logger 

logger = create_logger(os.path.join(os.path.dirname(os.path.abspath(__file__)),"worklog"), 'jiragetbug')

def get_jirabug(account,password,urls,bugstatus,filename=''):
    if urls=="":
        logger.info("url為空")
    else:
        urls=list(urls.split(','))
        JR=JIRA("https://pmo-jira.qyrc452.com/",basic_auth=(account,password))
        thisbugindex=["ID","BUG標題","創建者","狀態","BUG等級"]
        allbug=pd.DataFrame()
        if bugstatus==0: #未關單且未通過
            bugsearch='AND status != Closed AND status != pass'
        elif bugstatus==1: #未關單
            bugsearch='AND status != Closed'
        elif bugstatus==2 or bugstatus==3: #全BUG(未篩選)
            bugsearch=''

        for url in urls:
            issuekey=url.split("/")[-1]
            thisbug=JR.search_issues('issue in linkedIssues("'+issuekey+'") AND issuetype ="BUG"'+bugsearch, maxResults=-1)
            datas=[]
            for index,thisbug in enumerate(thisbug):
                thisbugcol=[str(thisbug.key), str(thisbug.fields.summary),str(thisbug.fields.reporter),str(thisbug.fields.status.name),str(thisbug.fields.priority)]
                datas.append(thisbugcol)

            thisbugdf=pd.DataFrame(datas,columns=thisbugindex)
            allbug=pd.concat([allbug,thisbugdf],ignore_index=True)
        allbug['BUG等級']=allbug['BUG等級'].map({'High':'A',
        'Highest':'A',
        'Medium':'B',
        'Low':'C',
        'Lowest':'C',
        })
        if bugstatus!=3 and filename!='':
            allbug.to_excel(filename,encoding='utf-8',index=False)
        
        return allbug

'''
if __name__ == "__main__":


    envlist='https://pmo-jira.qyrc452.com/browse/CRND02-563,https://jira.dlmd40.com/browse/CRND02-564,https://jira.dlmd40.com/browse/CRND02-529'

    allbug=get_jirabug('oliver206','XD6R247L',envlist,1,'C:\\Users\\oliverchiu\\Desktop\\packing\\jirabug-2.xlsx')
'''
