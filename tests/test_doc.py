# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-06
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from pathlib import Path
from novela.utils import rename_doc_and_save, get_sentences, sort_file
from matplotlib import cm

import docx
import re

def main():
    file = r"F:\实验室\网络小说信息抽取\sample_data\王妃.txt"
    # with open(file, "r", encoding="utf-8") as f:
    #     for i, line in enumerate(f):
    #         print(line)
    #         if i > 10:
    #             break
    # rename_doc_and_save(file)
    # get_sentences(file)
    # print(type(cm.get_cmap(name="viridis")))
    sentences = get_sentences(file)
    print(len(sentences))


def test_path():
    path = r"F:\实验室\网络小说信息抽取\sample_data"

    files = os.listdir(path)
    sort_files = sort_file(files)
    print(sort_files)


def test_re():
    str1 = '王妃6-7.docx'
    str2 = '王妃11.docx'
    pattern = re.compile(r"\d+")
    match = re.search(pattern, str2)
    print(type(match.group(0)))



if __name__ == '__main__':
    # main()
    # test_path()
    # test_re()
    print(globals())