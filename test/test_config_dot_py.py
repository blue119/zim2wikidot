#!/usr/bin/env python
# coding=utf-8

import sys
import tempfile
import xmlrpclib

from config import *


# config
# 參數: doc_root => 指向 zim 文件的根目錄
# 
# 1. 讀取 config 的設定
# all_config = config.get_all_config( doc_root ) 
#
# ?? all_config 的資料結構如何 ??
#
# 
# ?? 能否提供存取設定的方便函式 ??
# 
# 1. 讀取設定
# app_name, app_key = config.get_setting( "site's name" )
#
#   這裡記得加上 parsing check 的提示, 這樣子使用者才會知道那裡設錯了
#
#### 2. 儲存設定 ( 應該不會有，因為是用編輯器來存 )
#### config.set_setting( "site's name", app_name, app_key )
#
# doc_root ==> zim_root  這樣子會比較清楚

def main():
    doc_root = sys.argv[1]
    print doc_root

    all_config = get_all_config(doc_root)

    # FIXME: Let user select one of all_config. Now assume 0 is selected
    config = all_config[0]

    print config["h4_wikidot_creater"]


if __name__ == '__main__':
    main()
