#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import ConfigParser
import string, os, sys

def get_api_name_and_key( site ):
    result = None, None

    cf = ConfigParser.ConfigParser()
    config_file_path = os.path.join( os.getenv('HOME'), ".zim2wikidot.conf" )
    # TODO: 對 config_file 作 fail-safe
    cf.read( config_file_path )

    sec = site
    if cf.has_section( sec ):

        api_name = cf.get( sec, "api_name" )
        api_key  = cf.get( sec, "api_key" )
        if api_name != None and api_key != None:
            result = api_name, api_key

    return result

def get_template_file():
    result = None

    cf = ConfigParser.ConfigParser()
    config_file_path = os.path.join( os.getenv('HOME'), ".zim2wikidot.conf" )
    # TODO: 對 config_file 作 fail-safe
    cf.read( config_file_path )

    sec = "default"
    if cf.has_section( sec ):

        template_file = cf.get( sec, "template" )
        if template_file!= None:
            result = template_file

    return result


# 以上的部分是用於函式庫引用 import
# 以下的部分是用於個別的命令列執行測試
if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    config_file_path = os.path.join( os.getenv('HOME'), ".zim2wikidot.conf" )
    cf.read( config_file_path )

    # zim2wikidot 專用的設定區
    if cf.has_section("default"):
        sec = "default"
        opts0 = cf.options( sec )
        print '-'*20, "zim2wikidot 的設定區有", '-'*20
        
        for opt in opts0:
            print  opt, "=>", cf.get( sec, opt )
    else:
        print "沒有 zim2wikidot 的設定區"

    # 顯示
    secs = cf.sections()
    secs.remove( "default" ) # 去掉 "default" 的區
    print '各站的設定區有: ', secs
    
    for sec in secs:
        print '-'*30, sec, '-'*30

        opts = cf.options( sec )
        for opt in opts:
            print  opt, "=>", cf.get( sec, opt )
