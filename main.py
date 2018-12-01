# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:07:29 2017

@author: lizenghai
"""

import os,shutil,sys
import platform

thissys = platform.system()
FLAG = r'\\' if thissys == 'Windows' else '/'
pyver = sys.version_info[0] + sys.version_info[1]/10
MODICT = {'spyder':'spyder.mo',
          'spyder_pylint':'pylint.mo',
          'spyder_profiler':'profiler.mo',
		  'spyder_breakpoints':'breakpoints.mo'}
def checkpath(path):
    '''檢查路徑，如果路徑不存在則創建。
    param path<str>: 路徑位址。
    return <str>:經過檢查的路徑。
    '''
    try:
        tmp = path.split(FLAG)
        if '.' in tmp[-1] and len(tmp)>1:
            path = FLAG.join(tmp[:-1])
    except:
        pass
    if os.path.exists(path):
        if os.path.isfile(path)==False:
            return path
        else:
            raise ValueError('文件夾創建失敗，存在同名文件。')
    else:
        os.makedirs(path)
        return path


def search_packages_path(pyflag='1'):
    '''查找site-packages的路徑位址
    return <str>: path.
    '''
    sitepath="."
    for x in sys.path:
        if pyflag == '1' and 'anaconda' not in x.lower():
            continue
        if 'AppData' in x:
            continue
        ix1 = x.find('site-packages')
        ix2 = x.find('dist-packages')
        if( (ix1>=0 and x[ix1:]=='site-packages') or (ix2>=0 and x[ix2:]=='dist-packages') ):
          sitepath = x
          break
    
    return sitepath


def creat_language_folder(sitepath, modulename='spyder'):
    # creat zh_TW language folder
    try:
        zh_TW = sitepath + '{sep}{modulename}{sep}locale{sep}zh_TW{sep}LC_MESSAGES'.format(sep=FLAG, modulename=modulename)
        checkpath(zh_TW)
        
        return 1
    except:
        return 0
    
def shutil_file(sitepath, modulename='spyder'):
    mo_file_name = MODICT[modulename]
    zh_TW = sitepath + '{sep}{modulename}{sep}locale{sep}zh_TW{sep}LC_MESSAGES'.format(sep=FLAG, modulename=modulename)
    shutil.copyfile(mo_file_name,zh_TW + r'{0}{1}'.format(FLAG, mo_file_name))
    
def chinesize(sitepath):
    '''執行漢化'''
    # base.py add zh_TW
    configpath = sitepath + '{0}spyder{1}config{2}base.py'.format(FLAG,FLAG,FLAG)
    print(configpath)
    newpath = sitepath + '{0}base.py'.format(FLAG)
    # 根據作業系統（Windows和linux）、python2個大版本分別讀取配置信息
    # 2020年之後就好了
    if thissys == 'Windows':
        if pyver > 2.7:
            newf = open(newpath, 'w', encoding='utf-8')
            with open(configpath, 'r',encoding='utf-8') as f:
                lines = f.readlines()
        else:
            import io
            newf = io.open(newpath, 'w', encoding='utf-8')
            with io.open(configpath, 'r',encoding='utf-8') as f:
                lines = f.readlines()
    
        islanguage = 0
        for i in range(len(lines)):
            line = lines[i]
            newf.writelines(line)
            if "LANGUAGE_CODES = {'en': u'English'," in line:
                islanguage = 1
                mystr = "                  'zh_TW': u'繁體中文',\n" if pyver >2.7 else u"                  'zh_TW': u'繁體中文',\n"
                
                newf.writelines(mystr)
    
    else:
        newf = open(newpath, 'w')
        with open(configpath, 'r') as f:
            lines = f.readlines()
            islanguage = 0
        for i in range(len(lines)):
            line = lines[i]
            newf.writelines(line)
            if "LANGUAGE_CODES = {'en': u'English'," in line:
                #print(line)
                islanguage = 1
                mystr = "                  'zh_TW': u'繁體中文',\n"
                newf.writelines(mystr)
    newf.close()

    # rename old base.py
    if os.path.exists(sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG)):
        os.remove(sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG))
    os.rename(configpath,sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG)) 
    # remove new base.py
    shutil.move(newpath,configpath) 
    mystr = u'中文語言包安裝完畢，重啟後配置語言選項即可。 \n\n 按ENTER鍵開始子模塊漢化'
    pyinput(mystr)
    return

def pyinput(mystr):
    try:
        input_content = raw_input(mystr.encode('gbk'))
    except:
        input_content = input(mystr)
    return input_content

if __name__ == '__main__':
    mystr = u'請輸入數字以區分漢化方式，\n1、手動填入Python模塊包路徑（如：D:\Anaconda3\Lib\dist-packages 或 D:\Anaconda3\Lib\site-packages）。\n2、自動尋找路徑。\n請輸入 1或2:  '
    install_flag = pyinput(mystr)
    if install_flag == '1':
        mystr = u'Python安裝根路徑（如：D:\python 或 D:\anaconda）：  '
        sitepath = pyinput(mystr)
    else:
        mystr = '''
        =======================================================
        由於不同用戶的環境變量過於復雜難以完全兼顧，因此
        加入部分手動配置項。                    
        一般而言，只有Windows系统會比較麻煩。另外，如果你 
        是windows系统，請確保你的python不是安裝在系統盤中 
        的用戶文件夾下的AppData這一類的路徑裡，為了照顧到
        大多數人已經將AppData做了過濾。    
        
        
        注意！！！ 如果你在安装anaconda時修改了其文件夾名
        稱（如:默認為d:\\anaconda3,被修改為d:\\test），請按
        照選2/3，不要選1             
        ======================================================='''
        
        print(mystr)
        
        #==============================================================================
        mystr = u'請選擇您的python類別:\n     1.Anaconda \n     2.Python原版\n     3.其他\n您的選擇（數字）：'
        pyflag = pyinput(mystr)
   
        sitepath = search_packages_path(pyflag)
    
    print(sitepath)
    # 創建主翻譯
    creat_language_folder(sitepath, 'spyder')
    shutil_file(sitepath, 'spyder')
    chinesize(sitepath)
    
    # 創建子翻譯
    for m in MODICT.keys():
        if m =='spyder':
            continue
        creat_language_folder(sitepath, m)
        shutil_file(sitepath, m)

