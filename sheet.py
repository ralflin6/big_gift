# @Author: oliver
# @Date:   2021-03-26 16:24:06
# @Last Modified by:   oliver
# @Last Modified time: 2022-03-09 17:41
import os
#region 模組導入
import pygsheets
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

gc = pygsheets.authorize(service_account_file='key.json')
survey_url = 'https://docs.google.com/spreadsheets/d/1a3P-sZXj3PlzZC5W17zxmhhy2A9wz3qpKV2d_ZUzho8'
sh = gc.open_by_url(survey_url)
ws = sh.worksheet_by_title('this')

def return_sheet_value(sheet):
    logger.warning('開始抓取google表單資訊')
    val = ws.get_value(sheet,value_render='UNFORMATTED_VALUE')
    logger.warning('抓取完成')
    return val


def return_sheet_partment(start,end):
    """
    回傳值1為部門列表 回傳值2為環境列表
    """
    logger.warning('開始部門與環境列表')
    val=ws.get_values(start,end,value_render='UNFORMATTED_VALUE')
    val1=[]
    val2={}
    for i in list(set(val[1])):
        if i !='':
            val1.append(i)
            val2[i]=[]
    for i in range(len(val[0])):
        if val[1][i] != '':
            val2[val[1][i]].append(val[0][i])
    logger.warning('部門與環境列表抓取完畢')
    return val1,val2

#col可以抓列
def return_sheet_envinfo(env):
    
    envcol=ws.find(env)[0].col #顯示val列數
    key=ws.get_col(1,returnas='matrix')
    value=ws.get_col(envcol,returnas='matrix')
    dic={}
    for i in range(len(key)):
        dic[key[i]]=value[i]
    del dic['']
    logger.warning('回傳環境資料完畢')
    return dic



    


if __name__ == "__main__":
    print(return_sheet_envinfo('IN_外測'))