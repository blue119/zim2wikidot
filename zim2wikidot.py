#!/usr/bin/env python
# coding=utf-8

import sys
import os
import zim.fs
import zim.notebook
import zim.templates
import subprocess
import tempfile
import shutil
import pdb
import zim.exporter

from config import *

# notebook_path => NoteBook 的根目錄
# page_path     => 指定頁面的路徑,原始檔
# tmpfile_path  => 指定頁面的路徑,暫存檔
def main( notebook_path, page_path, tmpfile_path ):
    out_f = file( tempfile.mktemp(), 'a+' )

    # 設定轉出格式
    tmpl = zim.templates.get_template('wiki', '_New')
    #tmpl = zim.templates.get_template('html', 'Default')

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

    # 取得 ":xxx:yyy" zim 內用的頁面路徑
    p1 = nb.resolve_path( path )
    #pdb.set_trace()

    sys.stdout.writelines( tmpl.process(nb, p1) )

    out_f.writelines( tmpl.process(nb, p1) )
    out_f.close()

    cmd = "zenity --text-info --filename=" + out_f.name
    subprocess.Popen([ cmd ], shell=True ).communicate()

    
    # 執行完後，清掉暫存檔
    os.remove ( out_f.name )


## 將下列這一行，安裝至 custom tools 的項目:
##   $( readlink -f zim2wikidot.py) %f %d %s %n %D %t
##
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
