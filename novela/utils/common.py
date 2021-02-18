# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-05
import os
import re
import docx
import string
import jieba
import logging
import wordcloud
import numpy as np
from pathlib import Path
from matplotlib import colors
from win32com import client as winc
from typing import Set, List, Optional, Union, Callable

import novela.constants as constants


# 初始化结巴分词
jieba.initialize()


def get_wordcloud(font_path: str,  width: int = 400, height: int = 200, mask: Optional[np.ndarray] = None,
                  scale: float = 1.0, min_font_size: int = 4, max_font_size: int = None, max_words: int = 200,
                  min_word_length: int = 0, stopwords: Optional[Set[str]] = None, mode: str = "RGB",
                  relative_scaling: Union[float, str] = "auto", color_func: Optional[Callable] = None,
                  regexp: Optional[str] = None, collocations: bool = True, collocation_threshold: int = 30,
                  colormap: Union[str, colors.ListedColormap] = "viridis", normalize_plurals: bool = True,
                  repeat: bool = False, include_numbers: bool = False,
                  contour_width: float = 0.0, contour_color: str = "black",
                  background_color: str = "white"):
    """
    构造词云对象
    :param font_path: str型，表示字体文件的路径
    :param width: int型 (default=400)，画布的宽度
    :param height: int型 (default=200)，画布的高度
    :param mask: ndarray或者None，如果不是None，则是一个二进制的mask矩阵表示哪里可以绘制单词，并且此时会忽略width和height
    :param scale: float型 (default=1)，如果想要大一点的wordcloud，通过设置这个参数会更快，但是可能导致单词有点模糊
    :param min_font_size: int型 (default=4)，最小的单词的大小
    :param max_font_size: int型 (default=None)，最大单词的大小，如果是None，则使用上面指定的height
    :param max_words: int型 (default=200)，表示图中包含的最大单词数
    :param min_word_length: int型 (default=0)，表示单词的最小长度
    :param stopwords: Set[str] (default=None)，表示需要忽略的停用词，如果是None则使用内置的停用词
    :param mode: str型 (default="RGB")，如果mode="RGBA"并且background_color=None，那么绘制出来的图背景为透明
    :param relative_scaling: float型 (default='auto')，如果等于0，只考虑单词频率的排序；如果等于1，一个单词频率是另一个单词的两倍时，
                             对应的大小也是两倍；如果只想考虑频率不想考虑排序，最好设置为0.5左右；如果设置为'auto'，那么当repeat=True时，
                             等于0.5，否则为0
    :param color_func: callable (default=None)，需要包含word, font_size, position, orientation, font_path, random_state等
                       参数的可调用对象，对于每一个单词返回一个PIL的颜色，会重写"colormap"
    :param regexp: str型或者None (optional)，对应process_text方法中如果分割输入文本的正则表达式，默认为`r"\w[\w']+"`
    :param collocations: bool型 (default=True)，是否可以包含两个单词的组合（bigrams），如果使用generate_from_frequencies则忽略
    :param collocation_threshold: int型 (default=30)，如果一个bigram的Dunning似然组合分数大于这个参数，则算作bigram
    :param colormap: str型或者matplotlib colormap (default="viridis")，随机选择绘制每一个单词的颜色
    :param normalize_plurals: bool型 (default=True)，是否去除`'s`
    :param repeat: bool型 (default=True)，是否重复单词或者短语知道满足max_words或者min_font_size
    :param include_numbers: bool型 (default=False)，是否可以包含数字
    :param contour_width: float型 (default=0)，如果mask不是None，并且这个值>0，则会绘制mask轮廓
    :param contour_color: str型 (default="black")，表示mask轮廓的颜色
    :param background_color: str型 (default="white")，表示图片的背景颜色
    :return:
    """
    wc = wordcloud.WordCloud(font_path=font_path, width=width, height=height, mask=mask,
                             scale=scale, min_font_size=min_font_size, max_font_size=max_font_size,
                             max_words=max_words, min_word_length=min_word_length, stopwords=stopwords,
                             mode=mode, relative_scaling=relative_scaling, color_func=color_func,
                             regexp=regexp, collocations=collocations, collocation_threshold=collocation_threshold,
                             colormap=colormap, normalize_plurals=normalize_plurals, repeat=repeat,
                             include_numbers=include_numbers, contour_width=contour_width, contour_color=contour_color,
                             background_color=background_color)
    return wc


def get_sentences(file: str) -> List[str]:
    """
    读取文件，将文件中的语句或者段落保存
    :param file: str型，文件路径
    :return:
    """
    sentences = []
    if file.endswith(".docx"):
        document = docx.Document(file)
        for para in document.paragraphs:
            text = para.text.strip()
            if has_chinese(text):
                sentences.append(text)
    else:
        para = ""  # 用于记录段落
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                # 如果出现换行符，说明一段结束
                if line.endswith("\n"):
                    para += line.strip()
                    if has_chinese(para):
                        sentences.append(para)
                    para = ""
                else:
                    para += line.strip()
        # 最后判断是否存在遗漏
        if para and has_chinese(para):
            sentences.append(para)
    return sentences


def get_wordlist(sentences: List[str], stopwords: Set[str] = set()) -> List[str]:
    """
    将多个语句组成的列表转化为单词列表
    :param sentences: List[str]，每一个元素表示一个语句或者一个段落
    :param stopwords: Set[str]，表示停用词词表
    :return:
    """
    wordlist = []
    for sent in sentences:
        for word in jieba.cut(sent):
            word = word.strip()
            if word and has_chinese(word) and word not in stopwords and len(word) > 1:
                wordlist.append(word)
    return wordlist


def is_chinese_char(ch: str) -> bool:
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    cp = ord(ch)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
        (cp >= 0x3400 and cp <= 0x4DBF) or  #
        (cp >= 0x20000 and cp <= 0x2A6DF) or  #
        (cp >= 0x2A700 and cp <= 0x2B73F) or  #
        (cp >= 0x2B740 and cp <= 0x2B81F) or  #
        (cp >= 0x2B820 and cp <= 0x2CEAF) or
        (cp >= 0xF900 and cp <= 0xFAFF) or  #
        (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False


def is_english_char(ch: str) -> bool:
    """判断一个字符是否是英文字母"""
    cp = ord(ch)
    if (cp >= 0x41 and cp <= 0x5A) or (cp >= 0x61 and cp <= 0x7A):
        return True
    return False


def strQ2B(ustring: str) -> str:
    """
    全角符号转对应的半角符号
    :param ustring:
    :return:
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        # 全角空格直接转换
        if inside_code == 12288:
            inside_code = 32
        # 全角字符（除空格）根据对应的关系转换
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring


def is_chinese_punc(ch: str) -> bool:
    # 关于中文常用标点unicode编码 http://blog.chinaunix.net/uid-12348673-id-3335307.html
    puncs = [0xb7, 0xd7, 0x2014, 0x2018, 0x2019, 0x201c,
            0x201d, 0x2026, 0x3001, 0x3002, 0x300a, 0x300b,
            0x300e, 0x300f, 0x3010, 0x3011, 0xff01, 0xff08,
            0xff09, 0xff0c, 0xff1a, 0xff1b, 0xff1f]
    if ord(ch) in puncs:
        return True
    return False


def remove_space(ustring: str) -> str:
    """
    移除中文前后以及中间的空格，但是保留英文单词之间的空格
    :param ustring: str型
    :return:
    """
    ustring = ustring.strip()
    rstring = ""
    pre_ch = ""    # 保留空格位置前面第一个不为空格的字符

    s_len = len(ustring)
    for i in range(s_len):
        ch = ustring[i]
        if i == 0 or i == s_len - 1:
            rstring += ch
            pre_ch = ch
        else:
            # 如果当前字符不为空格
            if ch.strip():
                rstring += ch
                pre_ch = ch
            else:
                # 如果空格字符的前面和后面都是英文，则保留；
                # 否则去除该空格
                if (is_english_char(pre_ch) or pre_ch in string.punctuation) and (is_english_char(ustring[i+1])):
                    rstring += ch
    return rstring


def clean_text(ustring: str) -> str:
    """
    只保留字符串中的中文、英文字符、数字以及中英文常见标点
    :param ustring: str型，表示原始字符串
    :return:
    """
    # ustring = strQ2B(ustring)   # 这里将中文标点符号转化为英文标点，这里不需要
    # 移除一些无用的空格
    ustring = remove_space(ustring)
    rstring = ""
    for ch in ustring:
        if (is_chinese_char(ch) or is_chinese_punc(ch)) or \
                (is_english_char(ch) or (ch in string.punctuation)) \
                or (ch in string.digits) or (ch.isspace()):
            rstring += ch
    return rstring


def has_chinese(string: str) -> bool:
    """
    字符串中是否包含中文字符
    :param string:
    :return:
    """
    for ch in string:
        if is_chinese_char(ch):
            return True
    return False


def load_stopwords(file: str, extra_words: List[str] = None) -> Set[str]:
    """
    加载停用词文件
    :param file: str，表示文件路径名
    :param extra_words: List[str]，表示需要额外添加到停用词中的单词
    :return:
    """
    stopwords = set()
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                stopwords.add(line)
    if extra_words is not None:
        for ew in extra_words:
            stopwords.add(ew)
    return stopwords


def rename_doc_and_save(file: str):
    """
    将以.doc结尾的文件重命名为.docx结尾的文件，这样python才能读取
    :param file: str，文件路径
    :return:
    """
    path, file_name = os.path.split(file)
    file_wo_ext = file_name.split(".")[0]   # 去除扩展名的文件名称
    word = winc.Dispatch("Word.Application")
    document = word.Documents.Open(file)    # 读取文件
    new_file_name = file_wo_ext + ".docx"
    new_file = os.path.join(path, new_file_name)   # 新的文件名
    # 文件另存为
    document.SaveAs(new_file, 12, False, "", True, "", False, False, False, False)
    document.Close()
    word.Quit()
    # 将原文件删除
    os.remove(file)


def sort_file(file_list: List[str]) -> List[str]:
    """
    对文件按照章节顺序进行排序
    :param file_list:
    :return:
    """
    pattern = re.compile(r"\d+")
    indexes = []
    # 找到文件名中的第一个连续数字表示其起始章节
    for i, file in enumerate(file_list):
        match = re.search(pattern, file)
        if match is None:
            indexes.append((i, float(np.inf)))
        else:
            indexes.append((i, float(match.group(0))))

    sorted_indexes = sorted(indexes, key=lambda x: x[1])
    results = []
    for index in sorted_indexes:
        results.append(file_list[index[0]])
    return results


def repair_file(path: str, files: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    将.doc后缀修复为.docx后缀
    :param path: str型，路径名称
    :param files: str型或者List[str]，表示文件名
    :return:
    """
    def repair_one_file(file: str):
        if file.endswith(".doc"):
            rename_doc_and_save(os.path.join(path, file))
            file = file.replace(".doc", ".docx")
        return file

    if isinstance(files, str):
        return repair_one_file(files)
    elif isinstance(files, list):
        for i, file in enumerate(files):
            files[i] = repair_one_file(file)
        return files
    else:
        raise TypeError("Only str or List[str] can be recognized.")


def init_logger(log_file=None, log_file_level=logging.NOTSET, log_on_console=True):
    """用于初始化log对象，可以选择是否记录在文件中以及是否在屏幕上显示"""
    if isinstance(log_file, Path):
        log_file = str(log_file)

    log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                                   datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger(constants.PACKAGE_NAME)
    logger.setLevel(logging.INFO)
    if log_on_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.handlers = [console_handler]
    if log_file and log_file != "":
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    return logger