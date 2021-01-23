# coding=utf-8
# @Author: 莫冉
# @Date: 2020-12-31
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import numpy as np
import pandas as pd
from collections import Counter
from novela.utils import get_wordcloud, get_sentences, get_wordlist, load_stopwords, repair_file, sort_file
import novela.constants as constants
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import List

font_path = r"C:\Windows\Fonts\SIMLI.TTF"
simsong = fm.FontProperties(fname=font_path, size=10)


def autolabel(rects, ax):
    """
    对每个矩形进行标注
    :param rects:
    :return:
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")


def plot_bar(labels: List[str], y: List[int]):
    plt.rc("font", family="SimHei", size="15")
    plt.style.use("ieee")
    # 获取x轴标签的数量
    x = np.arange(len(labels))
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    rects = ax.bar(x, y, color="royalblue", alpha=0.7)

    # 添加一些标注
    ax.set_ylabel("词频", fontproperties=simsong)
    ax.set_ylim(0, 40)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontproperties=simsong)

    # 给矩形添加标注
    autolabel(rects, ax)
    # plt.show()
    fig.savefig("gender.png", bbox_inches="tight", dpi=300)



if __name__ == '__main__':
    # from matplotlib.pyplot import imread
    # pic_path = r"F:\实验室\网络小说信息抽取\图片\book.png"
    font_path = r"C:\Windows\Fonts\SIMLI.TTF"
    stopwords_file = "../data/resources/stopwords.txt"
    text_path = r"F:\实验室\网络小说信息抽取\sample_data"

    files = os.listdir(text_path)
    # print("origin files: ", files)
    # 首先对文件进行修复
    files = repair_file(text_path, files)
    # print("repair files: ", files)
    # 对文件名排序
    files = sort_file(files)
    # print("sort files: ", files)

    # 读取每个文件中的内容
    sentences = []
    for file in files:
        sentences.extend(get_sentences(os.path.join(text_path, file)))

    # --------------- 对于性别词的统计 ----------------
    gender = {}
    for sent in sentences:
        sent = sent.lower()
        gender[constants.SHE] = gender.get(constants.SHE, 0) + sent.count(constants.SHE)
        gender[constants.HE] = gender.get(constants.HE, 0) + sent.count(constants.HE)
        gender[constants.IT] = gender.get(constants.IT, 0) + sent.count(constants.IT)
        gender[constants.TA] = gender.get(constants.TA, 0) + sent.count(constants.TA)

    # ----------------------------------------------
    # 加载停用词
    stopwords = load_stopwords(stopwords_file)

    # 得到单词列表
    wordlist = get_wordlist(sentences, stopwords)

    word_count = Counter(wordlist)
    # 按照频率排序
    sort_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    # ----------------------------------------------
    # 将词频统计保存为表格
    words, counts = [], []
    for item in sort_words:
        words.append(item[0])
        counts.append(item[1])
    df = pd.DataFrame({"单词": words, "词频": counts})
    df.to_excel("词频统计.xlsx", index=False)

    # ---------------------------------------------
    # 绘图
    labels = list(gender.keys())
    y = list(gender.values())
    plot_bar(labels, y)

    # print(sort_words)
    # print(gender)

    # # # 初始化wordcloud
    # # mask = imread(pic_path)
    width = 1600
    height = 1000
    max_font_size = 400
    max_words = 80
    wc = get_wordcloud(font_path=font_path, width=width, height=height,
                       max_font_size=max_font_size, max_words=max_words)
    # 生成词云
    wc.generate(" ".join(wordlist))
    wc.to_file("wf.png")

