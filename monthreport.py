# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2021-11-18 11:05
# @Last Modified by:   oliver
# @Last Modified time: 2022-03-09 17:38

import os

from xlsxwriter import workbook
#region 模組導入
import pandas as pd
import xlwings as xw
import logging
import datetime
loglocation=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir,"worklog",str(datetime.date.today())+"log.txt"))
logging.basicConfig(
    filename=loglocation,
    level=logging.INFO,
    format='%(asctime)s- %(filename)s-%(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#endregion

def main(filename):
    logger.warning('開始修改月報')
    app = xw.App(visible=True,add_book=False)
    wb=app.books.open(filename)
    sht=wb.sheets['Month Report Sample']
    for i in range(sht.used_range.shape[0]):
        location=f'A{i+1}'
        if sht.range(location).value != None and ("底下的任務" in sht.range(location).value or "QA-294" in sht.range(location).value or "其他工作事項" in sht.range(location).value):
            sht.range(f'A{i+1}:J{i+1}').color = ('#3c78d8')
            sht.range(f'A{i+1}:J{i+1}').api.Font.Size=12
    sht.range('B1').column_width = 15
    sht.range('C1').column_width = 15
    sht.range('D1').column_width = 15
    sht.range('E1').column_width = 15
    sht.range('F1').column_width = 15
    sht.range('G1').column_width = 15
    sht.range('H1').column_width = 15
    sht.range('I1').column_width = 15
    sht.range('J1').column_width = 15
    
    sht.range('B:J').api.HorizontalAlignment = -4108
    sht.range('B:J').api.VerticalAlignment = -4108
    active_window = wb.app.api.ActiveWindow
    active_window.FreezePanes = False
    active_window.SplitColumn = 0
    active_window.SplitRow = 1
    active_window.FreezePanes = True

    wb.save()
    wb.close()

    app.quit()
    logger.warning('月報修改完畢')


if __name__ == "__main__":
    filename="D:/Month Report Sample.xls"
    main(filename)
