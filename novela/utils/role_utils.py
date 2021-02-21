# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-21
import jieba
import jieba.posseg as pseg
from typing import List
from collections import OrderedDict
import ngender

import novela.constants as constants
from novela._utils.typehint import OrderedDictType
from novela._utils.imports import LazyModule

try:
    from pyhanlp import HanLP
except:
    HanLP = LazyModule("HanLP", global_dict=globals())


def extract_names_hanlp(sentences: List[str]) -> OrderedDictType[str, List[int, str]]:
    """
    使用HaNLP中的实体识别模型，提取人名
    :param sentences: List[str]，表示所有的输入语句
    :return:
    """
    segment = HanLP.newSegment().enableNameRecognize(True)

    # 所有的名字到出现次数和位置的映射
    # 映射的值是一个list，第二个元素表示出现这个名字的句子
    names = OrderedDict()
    sentence_name_nums = []    # 表示每一个句子中出现的人名的数量
    for i, sent in enumerate(sentences):
        term_list = segment.seg(sent)
        name_count = 0
        for term in term_list:
            term_string = str(term)
            word, label = term_string.split("/")
            if label.startswith("nr"):
                name_count += 1
                if word in names:
                    names[word][0] += 1
                    names[word][1].append(i)
                else:
                    names[word] = [1, [i]]
        sentence_name_nums.append(name_count)

    # 判断姓名的性别
    for name, value in names.items():
        gender = judge_gender(name=name,
                              occur_indexes=value[1],
                              sentences=sentences,
                              sentence_name_nums=sentence_name_nums)
        names[name][1] = gender

    # 键名就是人名
    # 值的第一个元素为名字出现的次数
    # 值得第二个元素为名字的性别
    return names


def extract_names_jieba(sentences: List[str]) -> OrderedDictType[str, List[int, str]]:
    """
    使用jieba中的paddle模式获取人名
    :param sentences:
    :return:
    """
    jieba.enable_paddle()

    # 所有名字出现次数和位置的映射
    names = OrderedDict()
    sentence_name_nums = []
    for i, sent in enumerate(sentences):
        term_list = pseg.cut(sent, use_paddle=True)
        name_count = 0
        for word, label in term_list:
            if label == "PER" or label == "nr":
                name_count += 1
                if word in names:
                    names[word][0] += 1
                    names[word][1].append(i)
                else:
                    names[word] = [1, [i]]
        sentence_name_nums.append(name_count)

    # 判断姓名的性别
    for name, value in names.items():
        gender = judge_gender(name=name,
                              occur_indexes=value[1],
                              sentences=sentences,
                              sentence_name_nums=sentence_name_nums)
        names[name][1] = gender

    # 键名就是人名
    # 值的第一个元素为名字出现的次数
    # 值得第二个元素为名字的性别
    return names


def judge_gender(name: str,
                 occur_indexes: List[int],
                 sentences: List[str],
                 sentence_name_nums: List[int]):
    """
    判断这个名字的性别
    :param name: str，表示名字
    :param occur_indexes: 表示这个名字出现的句子的索引
    :param sentences: 表示各个句子
    :param sentence_name_nums: 表示该句子中出现名字的数量
    :return:
    """
    pronoun = {constants.HE: 0,
               constants.SHE: 0,
               constants.IT: 0,
               constants.TA: 0}
    for index in occur_indexes:
        # 如果这个句子中出现超过一个人名，则跳过
        if sentence_name_nums[index] > 1:
            continue

        for i, sent in enumerate(sentences[index:]):
            if i > 0 and sentence_name_nums[index+i] > 0:
                break
            # 计算各个人称代词出现的次数
            pronoun[constants.HE] += sent.count(constants.HE)
            pronoun[constants.SHE] += sent.count(constants.SHE)
            pronoun[constants.IT] += sent.count(constants.IT)
            pronoun[constants.TA] += sent.lower().count(constants.TA)

    if pronoun[constants.HE] != 0 or pronoun[constants.SHE] != 0:
        ratio = abs(pronoun[constants.HE] - pronoun[constants.SHE]) \
                / (pronoun[constants.HE] + pronoun[constants.SHE])
        if ratio > 0.2:
            if pronoun[constants.SHE] > pronoun[constants.HE]:
                return "女"
            else:
                return "男"
    elif pronoun[constants.IT] != 0 or pronoun[constants.TA] != 0:
        return "不确定"

    result = ngender.guess(name)[0]
    return result




