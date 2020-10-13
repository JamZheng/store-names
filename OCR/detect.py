#!/usr/bin/env python
# coding: utf-8

# 加载图片
# 文字检测 + 文字识别
# 结果写入txt文件

'''
参数：input_dir 图片所在的文件夹路径
output_txt 结果写入的的txt文件

输出单张图片检测用时以及平均用时
'''

import os
GPUID='1'##调用GPU序号
os.environ["CUDA_VISIBLE_DEVICES"] = GPUID
import torch
from apphelper.image import xy_rotate_box,box_rotate,solve
import cv2
import numpy as np
import time
from PIL import Image
import argparse
from glob import glob
#相关库的引入

import warnings 
warnings.filterwarnings("ignore")#忽略tf的版本警告

import model


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--input_dir', type=str, default = '')
parser.add_argument('--output_txt', type=str, default= './ocr_result.txt')
args = parser.parse_args()

print('input directory:' + str(args.input_dir))
print('output file:' + str(args.output_txt))

#文字检测展示函数
def plot_box(img,boxes):
    blue = (0, 0, 0) #18
    tmp = np.copy(img)
    for box in boxes:
         cv2.rectangle(tmp, (int(box[0]),int(box[1])), (int(box[2]), int(box[3])), blue, 1) #19
    
    return Image.fromarray(tmp) 

def plot_boxes(img,angle, result,color=(0,0,0)):
    tmp = np.array(img)
    c = color
    h,w = img.shape[:2]
    thick = int((h + w) / 300)
    i = 0
    if angle in [90,270]:
        imgW,imgH = img.shape[:2]
        
    else:
        imgH,imgW= img.shape[:2]

    for line in result:
        cx =line['cx']
        cy = line['cy']
        degree =line['degree']
        w  = line['w']
        h = line['h']

        x1,y1,x2,y2,x3,y3,x4,y4 = xy_rotate_box(cx, cy, w, h, degree/180*np.pi)
        
        x1,y1,x2,y2,x3,y3,x4,y4 = box_rotate([x1,y1,x2,y2,x3,y3,x4,y4],angle=(360-angle)%360,imgH=imgH,imgW=imgW)
        cx  =np.mean([x1,x2,x3,x4])
        cy  = np.mean([y1,y2,y3,y4])
        cv2.line(tmp,(int(x1),int(y1)),(int(x2),int(y2)),c,1)
        cv2.line(tmp,(int(x2),int(y2)),(int(x3),int(y3)),c,1)
        cv2.line(tmp,(int(x3),int(y3)),(int(x4),int(y4)),c,1)
        cv2.line(tmp,(int(x4),int(y4)),(int(x1),int(y1)),c,1)
        mess=str(i)
        cv2.putText(tmp, mess, (int(cx), int(cy)),0, 1e-3 * h, c, thick // 2)
        i+=1
    return Image.fromarray(tmp).convert('RGB')


#调用模型并计算模型调用时间
def ocr(p):
    img = cv2.imread(p)

    h,w = img.shape[:2]
    timeTake = time.time()
    _,result,angle= model.model(img,
                                        detectAngle=False,##不进行文字方向检测
                                        config=dict(MAX_HORIZONTAL_GAP=40,##字符之间的最大间隔，用于文本行的合并
                                        MIN_V_OVERLAPS=0.6,
                                        MIN_SIZE_SIM=0.6,
                                        TEXT_PROPOSALS_MIN_SCORE=0.1,
                                        TEXT_PROPOSALS_NMS_THRESH=0.3,
                                        TEXT_LINE_NMS_THRESH = 0.8,##文本行之间测iou值

                    ),
                                        leftAdjust=True,##对检测的文本行进行向左延伸
                                        rightAdjust=False,##对检测的文本行进行向右延伸
                                        alph=0.05,##对检测的文本行进行向右、左延伸的倍数

                                       )

    timeTake = time.time()-timeTake

    print('It take:{}s'.format(timeTake))
    #计算模型调用所花费时间
    
    #输出图片检测结果
    #for line in result:
    #    print(line,'\n')
    #plot_boxes(img,angle, result,color=(0,0,0))
    return img,result,angle,timeTake

#测试用
#p = './test/32.jpg'
#img,result,angle = ocr(p)
#plot_boxes(img,angle, result,color=(0,0,0))

time_sum = 0
roots= args.input_dir + '*.[j|p|J]*'
jpgPath = glob(roots)

if len(jpgPath) == 0:
    print("There is no picture")
    exit()
#将检测结果写入result.txt
with open(args.output_txt,"w") as f:
    for p in jpgPath:
        print(p)
        img,result,angle,timeTake = ocr(p)
        f.write(p + '\n' + str(result) + '\n')
        time_sum = time_sum + timeTake
f.close()

print('average time each image:',time_sum/len(jpgPath), 's')






