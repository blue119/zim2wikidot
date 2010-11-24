#!/usr/bin/env python
# coding=utf-8
#
# Author: Chun-Yu Lee (Mat) <matlinuxer2@gmail.com>
#

import sys
import os
import zim.fs
import zim.notebook
import zim.templates
import subprocess
import tempfile
import shutil
import pdb
import xmlrpclib 
import conf

def upload( site, page, title, content_file ):
    # site: 指定該頁面要上傳的 site
    api_app_name, api_app_key = conf.get_api_name_and_key( site )
       
    if api_app_name == None or api_app_key == None:
        return False

    content = ""
    for line in file(content_file):
        content += line

    #print('https://%s:%s@www.wikidot.com/xml-rpc-api.php' % ( api_app_name, api_app_key ) )
    #print({'site' : site, 'page' : page, 'title' : title, 'source' : content})
    srvProxy = xmlrpclib.ServerProxy('https://%s:%s@www.wikidot.com/xml-rpc-api.php' % ( api_app_name, api_app_key ) )
    srvProxy.page.save({'site' : site, 'page' : page, 'title' : title, 'source' : content})

    return True

# notebook_path => NoteBook 的根目錄
# page_path     => 指定頁面的路徑,原始檔
# tmpfile_path  => 指定頁面的路徑,暫存檔
def main( notebook_path, page_path, tmpfile_path ):
    out_d = tempfile.mkdtemp()
    out_f = file( tempfile.mktemp(), 'a+' )

    # TODO: format 跟 template 可能每個站的設定配對不同，應該要再加一個指定站的參數
    format_name_or_path = conf.get_format_file_or_name()
    format_file =  zim.fs.File( format_name_or_path )
    if format_file.exists() :
        name = format_file.basename
        if name[-3:] == ".py":
            name = name[:-3]
        sys.path.append( format_file.dir.path )
        format = __import__( name )
    else:
        format = format_name_or_path
    
    tmpl_file = conf.get_template_file()

    # 設定轉出格式跟範本
    #tmpl = zim.templates.get_template('wiki', '_New')
    #tmpl = zim.templates.get_template('html', 'Default')
    tmpl = zim.templates.get_template( format, zim.fs.File(tmpl_file) )
    # TODO: 在這裡檢查是否有正確取得 template exporter, 若沒有則提示錯誤

    # 選定 Notebook
    ##nb = zim.notebook.get_default_notebook()
    nb = zim.notebook.get_notebook( zim.fs.Dir( notebook_path ) )

    # 取得當前的頁面項目
    nb_path = nb.resolve_file( notebook_path, notebook_path )
    pg_path = nb.resolve_file( page_path, notebook_path )

    path_array = [u'']
    path_array += pg_path.relpath( nb_path ).split('/')
    #path = zim.notebook.Path( path_array )
    path = ':'.join( path_array )
    if path[-4:] == u".txt":
        path = path[:-4]

    # 取得 ":xxx:yyy" zim 內用的頁面路徑
    page = nb.get_page( nb.resolve_path( path ) )
    #pdb.set_trace()

    lines = tmpl.process(nb, page )

    #sys.stdout.writelines( l.encode('utf-8') for l in lines )
    out_f.writelines( l.encode('utf-8') for l in lines  )
    out_f.close()

    # 用 zim 來顯示結果
    cmd = "zenity --text-info --filename=" + out_f.name
    subprocess.Popen([ cmd ], shell=True ).communicate()

    # 上傳前，詢問確定
    cmd = 'zenity --question --text="確定要上傳?"; echo -n $?'
    answer = subprocess.Popen([ cmd ], shell=True, stdout=subprocess.PIPE ).communicate()[0]
    #print type( answer )
    #print answer
    if answer == "0":
        # TODO: 將 site, page, title 這三個參數用該頁的資料來取得 
        ret = upload( "hackingthursday", "test2", "zim 2 wikidot 上傳測試...", out_f.name )
        if ret == True:
            cmd = 'zenity --info --text="上傳完成"'
            subprocess.Popen([ cmd ], shell=True).communicate()
            
    else:
        # 取消上傳
        print "Cancel ..."
    
    # 執行完後，清掉暫存檔
    os.remove ( out_f.name )
    shutil.rmtree(out_d)


## 將下列這一行，安裝至 custom tools 的項目:
##   $( readlink -f zim2wikidot.py) %f %d %s %n %D %t
##
# TODO: 有幾項參數沒用到 %D, %t, 應該要簡化參數的設定
if __name__ == '__main__':
    if sys.argv.__len__() == 7:
        sys.argv[1]  # "%f: " => temperary
        sys.argv[2]  # "%d: " => file entry name
        sys.argv[3]  # "%s: " => real file path
        sys.argv[4]  # "%n: " => notebook
        sys.argv[5]  # "%D: " 
        sys.argv[6]  # "%t: " 
        
        print  sys.argv[4], sys.argv[3], sys.argv[1]
        main( sys.argv[4], sys.argv[3], sys.argv[1] )
