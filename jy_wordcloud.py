# coding:utf-8

from collections import Counter
from os import path
import jieba
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


"""
wordcloud==1.9.1.1
jieba==0.42.1
Pillow==9.5.0 
  即 PIL 包
"""

# 导入用户自定义词典(Load personalized dict to improve detect rate.)
jieba.load_userdict("./userdict.txt")

def word_segment(text):
    """
    对中文文本进行分词 (jieba 分词)
    返回分词后的字符串(空格分隔)
    """
    # 计算每个词出现的频率，并存入 txt 文件
    jieba_word = jieba.cut(text, cut_all=False)
    data=[]
    for word in jieba_word:
        data.append(word)
    dataDict = Counter(data)
    #print(dataDict)

    # 返回分词后的结果
    seg_list=' '.join(data)
    return seg_list


def generate_wordcloud(text, img_out, set_stopwords, bg_img=None, background_color="white", max_words=200):
    """
    text: 文本内容, 中文需经分词处理, 如:
          "引导 经济 全球化 朝着 更加 包容 互惠 、 公正 合理 的 方向 发展 。"
    """
    # 设置显示方式
    if bg_img:
        bg_mask = np.array(Image.open(bg_img))
    else:
        bg_mask = None
    font_path = "./font/msyh.ttf"
    wc = WordCloud(
            # 设置背景颜色
            background_color=background_color,
            # 词云显示的最大词数
            max_words=max_words, 
            # 设置背景图片
            mask=bg_mask,
            # 设置停用词
            stopwords=set_stopwords, 
            # 兼容中文字体，不然中文会显示乱码
            font_path=font_path,
            )

    # 生成词云
    wc.generate(text)

    # 生成的词云图像保存到本地
    wc.to_file(img_out)

    # 显示图像; interpolation='bilinear': 插值方法为双线性插值
    plt.imshow(wc, interpolation='bilinear')
    # 关掉图像的坐标
    plt.axis("off")
    plt.show()


if __name__=='__main__':
    # jy: 英文停用词
    #set_stopwords = set(STOPWORDS)
    # jy: 中文停用词
    ls_stopwords_cn = open("doc/stopwords-cn.txt").readlines()
    set_stopwords = set([word.strip() for word in ls_stopwords_cn if word.strip()])

    # 读取文件
    text = open("doc/19-da-report.txt").read()
    #text = open("doc/2017-zyzf.txt").read()
    #text = open("doc/alice.txt").read()

    #text="付求爱很帅并来到付求爱了网易研行大厦很帅 很帅 很帅"
    # 中文文本需先进行分词操作
    text = word_segment(text)
    # 生成词云
    # jy: 使用固定模板图片;
    #bg_img = "./images/alice_mask.png"
    # jy: 使用默认的矩形图片;
    bg_img = None
    img_out = "./images/zhonggong-19-da.png"
    generate_wordcloud(text, img_out, set_stopwords, bg_img)



