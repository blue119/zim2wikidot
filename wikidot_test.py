#!/usr/bin/env python
# -*= coding: utf-8 -*-

# 
# This example code is originally from: 幸延 <a0726h77@gmail.com>
#

from xmlrpclib import ServerProxy


# API_APP_NAME, API_APP_KEY: 一組 API 設定屬於一個帳號，同一組設定可以用於多個 site
api_app_name='API_APP_NAME'
api_app_key='API_APP_KEY'

# site: 指定該頁面要上傳的 site
site = 'SOME_SITE'

# page, title, content: 可以由該頁面的資料來取得
page = 'THE_PAGE'
title = 'THE_TITLE'
content = 'THE_CONTENT'

s = ServerProxy('https://%s:%s@www.wikidot.com/xml-rpc-api.php' % ( api_app_name,api_app_key ) )
s.page.save({'site' : site, 'page' : page, 'title' : title, 'source' : content})

# 執行完畢後，顯示上傳頁面的連結，供方便點擊前往
print 'To view : http://%s.wikidot.com/%s' % (site, page)
