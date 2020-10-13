import jieba
import jieba.analyse
import jieba.posseg
import codecs,sys
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__=='__main__':
    f = codecs.open('wiki.zh.simp.txt','r',encoding='utf-8')
    target = codecs.open('wiki.zh.simp.seg.txt','w',encoding='utf-8')
    print 'open files.'

    linenum=1
    line = f.readline()
    while line:
        print '-----processing ',linenum,' article---'
        seg_list = jieba.cut(line,cut_all=False)
        line_seg = ' '.join(seg_list)
        target.writelines(line_seg)
        linenum = linenum + 1
        line = f.readline()
    print 'well done'
    f.close()
    target.close()