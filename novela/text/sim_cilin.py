# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-29
from typing import Dict, List, Tuple
import numpy as np
import math
import jieba
from functools import lru_cache

from novela import logger


logger = logger.getChild("cilin")


class CilinSimilarity(object):
    """
    @desc:使用基于信息内容的算法来计算词语相似度。参考文献：
    【1】彭琦, 朱新华, 陈意山,等. 基于信息内容的词林词语相似度计算[J]. 计算-机应用研究, 2018(2):400-404.
    """
    def __init__(self, cilin_file: str = "../../data/resources/new_cilin.txt"):
        self.code_word: Dict[str, List[str]] = {}      # 以编码为key，单词list为value的dict，一个编码有多个单词
        self.word_code: Dict[str, List[str]] = {}      # 以单词为key，编码为value的dict，一个单词可能有多个编码
        self.vocab = set()                             # 所有不重复的单词，便于统计词汇总数
        self.file = cilin_file                         # 表示词林文件的路径
        self.mydict: Dict[str, int] = {}                               # 每一个大中小类编码对应的下位节点数量
        # 读取文件并进行统计
        self._read_cilin()
        # 计算总的节点数
        total = 0
        for ele in self.mydict:
            if len(ele) == 1:
                total += self.mydict[ele]

        logger.info(f"词林的总节点数为: {total}")
        # 得到计算信息内容含量时的分母
        self.fenmu = math.log(total, 2)

    def _read_cilin(self):
        """
        读取同义词词林，编码为key，词群为value，保存到self.code_word
        单词为key，编码群为 value，保存到self.word_code
        所有单词保存在self.vocab
        :return:
        """
        head = set()
        with open(self.file, "r", encoding="gbk") as f:
            for line in f:
                line = line.strip()
                res = line.split()
                code = res[0]        # 对应词义编码
                words = res[1:]      # 对应同一个编码的多个词
                self.vocab.update(words)       # 一组词更新到词汇表中
                self.code_word[code] = words   # 键是词义编码，值是同一个编码的一组词

                # 以单词为键，编码为值保存到self.word_code中
                for w in words:
                    if w in self.word_code:
                        # 如果单词存在于字典中，则把当前编码增加到字典中
                        self.word_code[w].append(code)
                    else:
                        # 否则，则在字典中添加该项
                        self.word_code[w] = [code]

                # 第一次遍历：得到大中小类的代码
                if len(code) < 6:
                    continue
                fathers = [code[:1], code[:2], code[:4], code[:5], code[:7]]
                head.update(fathers)
        # 得到排序之后的大中小类代码
        fatherlist = sorted(list(head))
        for ele in fatherlist:
            self.mydict[ele] = 0

        # 第二次遍历：得到大中小类的数量，更新到mydict中
        with open(self.file, "r", encoding="gbk") as f:
            for line in f:
                line = line.strip()
                res = line.split()
                code = res[0]      # 单词编码
                words = res[1:]    # 编码对应的单词列表
                if len(code) > 5 and code[:5] in self.mydict:
                    self.mydict[code[:7]] += len(words)
                    self.mydict[code[:5]] += len(words)
                if len(code) > 4 and code[:4] in self.mydict:
                    self.mydict[code[:4]] += len(words)
                if len(code) > 2 and code[:2] in self.mydict:
                    self.mydict[code[:2]] += len(words)
                if len(code) > 1 and code[:1] in self.mydict:
                    self.mydict[code[:1]] += len(words)

    def get_common_str(self, c1: str, c2: str):
        """
        计算两个字符的公共部分，注意有些层是2位数字
        这里的c1和c2都是编码
        """
        res = ""
        for i, j in zip(c1, c2):
            if i == j:
                res += i
            else:
                break

        if len(res) == 3 or len(res) == 6:
            res = res[:-1]
        return res

    @lru_cache(maxsize=32)
    def Info_Content(self, concept: str):
        """
        计算一个编码的信息内容含量
        这里的concept也是编码
        """
        if concept == "":
            return 0

        # 计算当前编码的下位节点数
        hypo = 1
        if concept in self.mydict:
            hypo += self.mydict[concept]
        info = math.log(hypo, 2) / self.fenmu
        # 下位节点数越多，信息含量越少；下位节点数越少，信息含量越高
        return 1 - info

    def sim_by_IC(self, c1: str, c2: str):
        # 找到公共字符串
        LCS = self.get_common_str(c1, c2)
        distance = self.Info_Content(LCS) - (self.Info_Content(c1) + self.Info_Content(c2)) / 2
        return distance + 1

    def word_sim(self, w1: str, w2: str) -> float:
        """
        计算两个单词的相似度，相似度范围在0-1之间（根据原始论文证明可以得到）
        -1.0表示有单词在词表中不存在
        """
        for word in [w1, w2]:
            if word not in self.vocab:
                logger.info(f"`{word}`没有被词林收录！")
                return -1.0

        # 获取两个单词的编码列表
        code1 = self.word_code[w1]
        code2 = self.word_code[w2]
        simlist = []
        for c1 in code1:
            for c2 in code2:
                cur_sim = self.sim_by_IC(c1, c2)
                simlist.append(cur_sim)
        average = sum(simlist) / len(simlist)
        # 按照规则返回相似度
        if len(simlist) < 2:
            return simlist[0]

        if max(simlist) > 0.7:
            return max(simlist)
        elif average > 0.2:
            return (sum(simlist) - max(simlist)) / (len(simlist) - 1)
        else:
            return min(simlist)

    def wordlist_sim(self, word_list1: List[str], word_list2: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        similarities, masks = [], []

        for w1 in word_list1:
            sims = []
            mask = []
            if w1.endswith("类"):
                w1 = w1[:-1]
            # 由于有的标签的中文单词很长
            # 所以需要分割分别判断
            w1_list = jieba.lcut(w1)
            for w2 in word_list2:
                sim_list = []
                for w in w1_list:
                    sim_list.append(self.word_sim(w, w2))
                if len(sim_list) == 1:
                    sim = sim_list[0]
                else:
                    sim = max(sim_list)
                if sim == -1.0:
                    mask.append(0.0)
                else:
                    mask.append(1.0)
                sims.append(sim)

            similarities.append(sims)
            masks.append(mask)

        return np.asarray(similarities), np.asarray(masks)



if __name__ == '__main__':
    cilin_file = "../../data/resources/new_cilin.txt"
    cilin = CilinSimilarity(cilin_file)

    print(cilin.word_sim("开心", "心酸"))
