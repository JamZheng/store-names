import os
import codecs
import sys
#oldfile:UTF8文件的路径
#newfile:要保存的ANSI文件的路径
def convertUTF8ToANSI(oldfile,newfile):

    打开UTF8文本文件
    f = codecs.open(oldfile,'r','utf8')
    utfstr = f.read()
    f.close()
    
    #把UTF8字符串转码成ANSI字符串
    outansestr = utfstr.encode('mbcs')

    #使用二进制格式保存转码后的文本
    f = open(newfile,'wb')
    f.write(outansestr)
    f.close()
if __name__=='__main__':
    inpath=sys.argv[1]
    outpath=sys.argv[2]
    convertUTF8ToANSI(inpath,outpath)