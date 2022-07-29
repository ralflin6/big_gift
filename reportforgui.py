# @Author: oliver
# @Date:   2021-04-01 18:04:30
# @Last Modified by:   oliver
# @Last Modified time: 2022-05-09 16:49

#Version:1.2.1

import os
#region 模組導入
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import logging
from argparse import ArgumentParser
import zipfile

loglocation=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"worklog",str(datetime.date.today())+"log.txt"))
logging.basicConfig(
    filename=loglocation,
    level=logging.INFO,
    format='%(asctime)s- %(filename)s-%(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)



#endregion

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#計畫:先讀取，把所有玩家資料變成一個DataFrame(未篩選)
#desan是脫敏還原功能 speedata是萬場資料用
def Combine(path):
    #抓取非目錄的所有資料
    allFileList=os.listdir(path)
    alldata=pd.concat([pd.read_excel(path+f) for f in allFileList])
    alldata.drop_duplicates(inplace=True) #去重複
    alldata.reset_index(inplace=True,drop=True) #重新編排index
    print('檔案融合完成')
    return alldata

def folder(location):
    if not os.path.isdir(location):
        os.mkdir(location)

def main(path,validbetno='11',winloseno='12',roomname_switch=False,commission_switch=False,RTP_switch=False,averagewin_switch=False):
    """
    path=修改為資料名稱，因為 Jenkins 不能上傳整包資料
    validbetno=有效投注欄位(預設11)
    winloseno=輸贏金額欄位(預設12)
    roomname_switch=是否開啟房間名
    commission_switch=是否開啟抽水
    RTP_switch=是否開啟RTP
    averagewin_switch=是否開啟場均輸贏
    """
    if os.path.isdir('./Chart_data_overview'): #如果原本存在就先移除，避免抓取到之前的資料
        import shutil #如果原本存在就先移除，避免抓取到之前的資料
        shutil.rmtree('./Chart_data_overview')
    if '.zip' in path :  #先把上傳上來的 Zip 檔案解壓縮
        with zipfile.ZipFile(f"./packing.zip", 'r') as zip:
            path = path.replace('.zip','')
            zip.extractall(f'./{path}') 

    dic={}
    total_dic={}
    if path[-1] != "/":
        realpath =path + "/"
    else:
        realpath=path
    alldata=Combine(realpath)
    playerlist=alldata.iloc[:,1].unique()
    if roomname_switch:
        print(realpath)
        folder(realpath.rsplit('/',2)[0]+'/'+alldata.iloc[:,4][0])
        output_path=realpath.rsplit('/',2)[0]+'/'+alldata.iloc[:,4][0]+'/Chart_data_overview/'
    else:
        output_path=realpath.rsplit('/',2)[0]+'/Chart_data_overview/'
    folder(output_path)
    
    alldata.sort_index(axis=0,inplace=True,ascending=False)
    
    output_excel_path=output_path+'總覽資料.xlsx'

    writer=pd.ExcelWriter(output_excel_path,engine='xlsxwriter')

    #sheet1(Total)
    total_validbet=alldata.iloc[:,int(validbetno)-1].astype(float).sum()
    total_winlose=alldata.iloc[:,int(winloseno)-1].astype(float).sum()
    total_commission=alldata.iloc[:,int(winloseno)].astype(float).sum()
    total_play=len(alldata.index)
    average_win=round(total_winlose/total_play,5)
    total_RTP=round((total_validbet+total_winlose)/total_validbet,5)
    total_index=['總有效投注','總輸贏','總場次']
    total_report=[total_validbet,total_winlose,total_play]
    if commission_switch:
        total_index.append('總抽水')
        total_report.append(total_commission)        
    if averagewin_switch:
        total_index.append('平均輸贏金額')
        total_report.append(average_win)
    if RTP_switch:
        total_index.append('RTP')
        total_report.append(total_RTP)
    

    total_dic['Total']=pd.Series(total_report,index=total_index)
    df_total=pd.DataFrame(total_dic)
    df_total.T.to_excel(writer,sheet_name='Total',index=True)
    print('Total寫入完成')
    
    #sheet2(separate) 各帳號分開的資訊
    for i in playerlist:
        df=alldata[alldata.iloc[:,1]==i]
        df.reset_index(inplace=True,drop=True)
        player_validbet=df.iloc[:,int(validbetno)-1].astype(float).sum()
        player_winlose=df.iloc[:,int(winloseno)-1].astype(float).sum()
        player_commission=df.iloc[:,int(winloseno)].astype(float).sum()
        player_play=len(df.index)
        player_average_win=round(player_winlose/player_play,5)
        player_RTP=round((player_validbet+player_winlose)/player_validbet,5)
        player_index=['總有效投注','總輸贏','總場次']
        player_report=[player_validbet,player_winlose,player_play]
        if commission_switch:
            player_index.append('玩家總抽水')
            player_report.append(player_commission)
        if averagewin_switch:
            player_index.append('平均輸贏金額')
            player_report.append(player_average_win)
        if RTP_switch:
            player_index.append('RTP')
            player_report.append(player_RTP)
        dic[i]=pd.Series(player_report,index=player_index)
    player_total=pd.DataFrame(dic)
    player_total.T.to_excel(writer,sheet_name='各帳號資料',index=True)
    Total_sheet=writer.sheets['Total']
    Player_sheet=writer.sheets['各帳號資料']
    Total_sheet.set_column('A:H', 15)
    Player_sheet.set_column('B:H', 15)
    Player_sheet.set_column('A:A', 25)
    wb=writer.book
    img_num=0
    Table_sheet=wb.add_worksheet('各帳號走勢圖')
    print('各帳號走勢圖寫入完成')

    for i in playerlist:
        df=alldata[alldata.iloc[:,1]==i]
        df.reset_index(inplace=True,drop=True)
        df=df.iloc[:,int(winloseno)-1]  #把不必要的資料拿掉 方便繪圖
        df2=df.cumsum()
        x1=df2[df2 >=0]
        x2=df2[df2<0]
        plt.figure(figsize=(20, 4)) #表格大小(x,y)
        plt.ticklabel_format(style='plain') #取消科學記號
        plt.scatter(x1.index,x1,c='red' , marker=',' ,s=1)
        plt.scatter(x2.index,x2,c='blue', marker=',' ,s=1)
        plt.plot(df.index,0*(df),lw=5,c='black')#設定0為一條線
        plt.grid(True)
        plt.title(i) #設定標題
        plt.xlabel("場數")
        plt.ylabel("累計輸贏金額")
        plt.savefig(output_path+i+'.png')
        #plt.show()
        Table_sheet.insert_image(img_num,0,output_path+i+'.png')
        img_num+=20
    writer.save()
    print('圖片輸出並貼入EXCEL完成')
    alldata.drop(index=df.index, inplace=True)
    pass
    zip_folder('./Chart_data_overview')
    
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
    parser.add_argument('--file_name', '-file', default='', type=str, required=False, help='file name')
    parser.add_argument('--para_set', '-paraset', default='', type=str, required=False, help='Parameter setting')
    parser.add_argument('--validbetno', '-betno', default='', type=str, required=False, help='valid bet number')
    parser.add_argument('--winloseno', '-wlno', default='', type=str, required=False, help='win lose number')
    return parser.parse_args()

if __name__ == "__main__":
    #path="C:/Users/ralflin/Desktop/大禮包v1.2.6"
    args = parse_args() #從外部取值
    path = args.file_name #導入的資料夾名稱
    commission_switch = RTP_switch = averagewin_switch = False
    if '1' in args.para_set:
        commission_switch = True
    if '2' in args.para_set:
        RTP_switch = True
    if '3' in args.para_set:
        averagewin_switch = True
    validbetno = args.validbetno
    winloseno = args.winloseno
    main(path='./'+path+'.zip',validbetno=validbetno,winloseno=winloseno,commission_switch=commission_switch,RTP_switch=RTP_switch,averagewin_switch=averagewin_switch)
