# -*- coding: utf-8 -*-
# @Author: oliver
# @Date:   2022-03-09 14:48
# @Last Modified by:   oliver
# @Last Modified time: 2022-03-09 15:20


def main():
    import os
    print('檢查必要套件，缺少時將嘗試自動進行安裝。')
    os.system(f'pip install -r requirements.txt | find /V "already satisfied"')
    import sys
    sys.tracebacklimit = 0
        


if __name__ == "__main__":
    main()
