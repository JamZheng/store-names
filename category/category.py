#coding:utf-8
import re
import yaml
import json
import gensim
import jieba
import sys


fmodel=sys.argv[1]
inf=sys.argv[2]
ouf=sys.argv[3]
Mode=sys.argv[4]
if not "model" in fmodel:
    raise IOError('The model is not exist!')
if not "txt" in inf:
    raise IOError('The pretxt is not exist!')
if len(ouf)==0:
    raise IOError('The outpath error!')

model=gensim.models.Word2Vec.load(fmodel)

f = open(inf,'r')
txt=f.read()

txt=re.sub("./train/data/text/0/","",txt)

# txt=re.sub("\(","",txt)
# txt=re.sub("\)","",txt)
txt=re.sub("\], \d+","",txt)
txt=re.sub("\[","",txt)

txt=txt.split('\n')[:-1]
# print txt[3]
ftest=open(ouf,"w")
if Mode.lower()=="--csv":
    ftest.write("\xEF\xBB\xBF")
ftest.write("图片,商铺名称\n")
cnt=0

for x in txt:
    if len(x)>0 and x[-1]!='g':
        cnt=cnt+1
        x=x.split(', ')
        words=[]
        width=[]
        height=[]
        best=0
        label=0
        for j in x:
            if j.find('text')!=-1:
                words=words+re.findall(": '(.*?)'",j,re.S)
            if j.find("'w'")!=-1:
                width=width+[float(re.findall("'w': (\d+.\d+)",j,re.S)[0])] 
            if j.find("'h'")!=-1:
                height=height+[float(re.findall("'h': (\d+.\d+)",j,re.S)[0])] 
        for k in range(len(words)):
            p=jieba.cut(words[k])
            score=0
            for i in p:
                try:
                    score=max(score,model.similarity(i,u"店名"))
                    score=max(score,model.similarity(i,u"产品"))  
                    score=max(score,model.similarity(i,u"商店"))  
                    score=max(score,model.similarity(i,u"工厂"))
                    score=max(score,model.similarity(i,u"银行"))  
                    score=max(score,model.similarity(i,u"餐饮"))
                    score=max(score,model.similarity(i,u"公司"))
                except:
                    pass
            #print score,words[k],width[k]*height[k]
            if best<width[k]*height[k]*score  and len(words[k])<=45:
                best = width[k]*height[k]*score
                label=k
            if best<width[k]*height[k]*0.3 and score==0 and len(words[k])<=10:
                best = width[k]*height[k]*0.3
                label=k
        try:
            s=number+','+words[label]+'\n'
            ftest.write(s)
        except:
            pass
    else:
        number=x

ftest.close()

# i=1
# words=[]
# for line in f.readlines():
#     lst=line.split('.jpg')
    
#     if str(i)==lst[0]:
#         words.append(lst[1])
#     else:
#         print words
#         print '----'
#         words=[lst[1]]
#         i+=1
