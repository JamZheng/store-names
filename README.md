# 街景企业实体识别任务

## 文字检测+文字识别部分

### 环境配置

测试环境：ubuntu 18.04 cuda 10.1 cdnn 7.5  python3

依赖库：opencv-contrib-python==4.0.0.21 Cython h5py lmdb mahotas pandas requests bs4 matplotlib lxml pillow  web.py==0.40.dev0 

redis  

* 训练部分：ubuntu 18.04 cuda 10.0 cdnn 7.5 依赖库：python3 tensorflow==1.8 numpy==1.14 

* 识别部分：keras==2.1.5 tensorflow==1.8.0  torch==1.6.0+cu101  torchvision==0.7.0+cu101

测试环境搭建：

```bash
pip install easydict opencv-contrib-python==4.0.0.21 Cython h5py lmdb mahotas pandas requests bs4 matplotlib lxml
pip install -U pillow
pip install web.py==0.40.dev0 redis 
pip install keras==2.1.5 tensorflow==1.8
pip install torch torchvision
```

### 使用说明

在根目录命令行中运行以下格式语句：

```bash
python detect.py --input_dir <input directory path> --output_txt <output file path>
```

例（读取组委会所提供的图片集，输出信息保存至根目录下 ocr_result.txt 文件中）：

```bash
python detect.py --input_dir ./train/data/text/t/ --output_txt ocr_result.txt
```



## 企业名称实体识别部分

### 环境配置

python2 gensim jieba pyyaml 

测试环境搭建：

```bash
sudo apt-get install python2 python-pip 
pip install gensim jieba pyyaml
```

### 使用说明

直接在 category 目录下 运行 category.py 其中<wiki-zh-txt-model path> <txtinputfile> <outputfile> 为必须。

```bash
python2 category.py <wiki-zh-txt-model path> <txtinputfile> <outputfile> <mode>
python2 .\category.py ./wiki.zh.text.model ./txtresult/OCR3result.txt ./out/name.csv --csv # example
```

结果将保存在./out/name.csv

注：如果要在windows下Excel查看，则要加上UTF-8 BOM 头，则带--csv参数，如果其他方式查看，打开就不需要用到此参数。



### reference

- https://github.com/chineseocr/chineseocr

- https://github.com/chongshengzhang/shopsign

- https://github.com/cgvict/roLabelImg

  