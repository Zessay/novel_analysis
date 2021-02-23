# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-01
from typing import Dict, List, Tuple
import math
import jieba
import numpy as np
from functools import lru_cache

from novela import logger


logger = logger.getChild("hownet")


def parseZhAndEn(text: str):
    """
    HowNet中单词是按照 en|zh 的方式组织的，所以要分割开
    """
    words = text.split("|")
    if len(words) == 2:
        return words[1], words[0]
    else:
        return text, text


class GlossaryElement:
    """
    表示词汇表文件中的每一项，即glossary中的每一项
    输入形式为：单词/词性/DEF表达式
    """
    def __init__(self):
        self.word = ""           # 词
        self.word_pos = ""       # 词性
        self.solid = False       # True是实词，False是虚词
        self.s_first = ""        # 第一基本义原
        self.s_other = []        # 其他义原
        self.s_relation = {}     # 关系义原
        self.s_symbol = {}       # 符号义原

    def print(self):
        """
        打印自身
        :return:
        """
        print(self.word + ", " + self.word_pos + ", | first: " + self.s_first + " | other: ")
        for i in range(len(self.s_other)):
            print(self.s_other[i] + ", ")

        print(" | relation: ")
        for it in self.s_relation.keys():
            print(it + "=" + self.s_relation[it] + ", ")

        print(" | symbol: ")
        for it in self.s_symbol.keys():
            print(it + "=" + self.s_symbol[it] + ", ")

        print("\n")

    def parse(self, text: str):
        text = text.strip()

        # 如果本行为空，则返回False；不为空则进行解析
        if len(text) <= 0:
            return False

        items = text.split("/")
        if len(items) == 3 and len(items[0]) > 0:
            self.word = items[0]       # 第一个元素是单词本身
            self.word_pos = items[1]   # 第二个元素是词性
            # 如果DEF表达式以`{`开头，说明是虚词；否则是实词
            if items[2].startswith("{"):
                self.solid = False
            else:
                self.solid = True

            # 将DEF表达式进行分割，得到每一个义原
            sememes = items[2].split(",")
            # 如果是虚词，即self.solid=False
            # 那么第一个义原应该以`{`起始，以`}`结束
            # 此时需要去除第一个义原前后的`{}`
            # 如果没有则不会去除
            sememes[0] = sememes[0].lstrip("{").rstrip("}")

            if len(sememes) > 0:
                firstdone = False
                # 如果第一个字母是英文
                # 这里得到第一义原
                if sememes[0][0].isalpha():
                    self.s_first, defaultText = parseZhAndEn(sememes[0])
                    firstdone = True

                # 处理其他义原
                # 如果以`(`开头，说明是其他独立义原；
                # 如果存在`=`，说明是关系义原；
                # 如果以非字母的其他符号开头，说明是符号义原；
                # 如果以字母开头，说明是其他独立义原。
                for i in range(len(sememes)):
                    if i == 0 and firstdone:
                        continue

                    firstletter = sememes[i][0]
                    if firstletter == "(":
                        self.s_other.append(sememes[i])
                    else:
                        equalpos = sememes[i].find("=")
                        if equalpos != -1:
                            key = sememes[i][:equalpos]
                            value = sememes[i][equalpos+1:]
                            # 有时候，值的两边可能是`()`，所以要去除
                            value = value.lstrip("(").rstrip(")")
                            if len(value) > 0:
                                value, defaultText = parseZhAndEn(value)
                            self.s_relation[key] = value
                        elif firstletter.isalpha():
                            self.s_other.append(sememes[i])
                        else:
                            value = sememes[i][1:]
                            value = value.lstrip("(").rstrip(")")
                            if len(value) > 0:
                                value, defaultText = parseZhAndEn(value)
                            self.s_symbol[firstletter] = value
            return True

        return False


class SememeElement:
    """
    表示关系义原中关系的每一项，即`WHOLE.DAT`文件
    """
    def __init__(self):
        self.id = -1         # 编号
        self.father = -1     # 父义原编号
        self.sememe_zh = ""  # 中文义原名称
        self.sememe_en = ""  # 英文义原名称

    def parse(self, text: str):
        text = text.strip()
        if len(text) <= 0:
            return False
        items = text.split()
        if len(items) == 3:
            self.id = int(items[0])
            self.father = int(items[2])
            self.sememe_zh, self.sememe_en = parseZhAndEn(items[1])
            return True
        return False


def valuesOfGlossaryTable(glossary_table: Dict[str, GlossaryElement], word: str):
    values = []
    for k, v in glossary_table.items():
        k = k.split("_")[1]
        if k == word:
            values.append(v)
    return values


class HowNetSimilarity:
    """
    基于知网义项树路径的单词相似度
    """
    def __init__(self,
                 glossary_file: str = "../../data/resources/glossary.txt",
                 sememe_file: str = "../../data/resources/WHOLE.DAT"):
        self.sememe_table = dict()        # 义原表
        self.sememeindex_zh = dict()      # 义原索引（中文）
        self.glossary_table = dict()       # 词汇表
        # 文件路径
        self.glossary_file = glossary_file
        self.sememe_file = sememe_file
        self.vocab = set()       # 保存所有单词
        self.BETA = [0.5, 0.2, 0.17, 0.13]
        self.GAMA = 0.2
        self.DELTA = 0.2
        self.ALFA = 1.6
        self.init()

    def init(self):
        if not self._load_sememe_table(self.sememe_file):
            logger.error(f"`{self.sememe_file}`文件加载失败！")
            return False
        if not self._load_glossary(self.glossary_file):
            logger.error(f"`{self.glossary_file}`文件加载失败！")
            return False
        return True

    def _load_sememe_table(self, filename: str):
        """加载义原表"""
        with open(filename, "rt", encoding="utf-8") as f:
            try:
                for line in f:
                    line = line.strip()
                    if line:
                        ele = SememeElement()
                        if ele.parse(line):
                            self.sememe_table[ele.id] = ele
                            self.sememeindex_zh[ele.sememe_zh] = ele
                logger.info("Load sememe file successfully!")
            except Exception as e:
                logger.error("Function load_sememe_table has errors!")
                logger.error(e)
                return False

        return True

    def _load_glossary(self, filename: str):
        """加载词汇表"""
        with open(filename, "r", encoding="utf-8")  as f:
            try:
                count = 0
                for line in f:
                    line = line.strip()
                    if line:
                        ele = GlossaryElement()
                        if ele.parse(line):
                            self.glossary_table[f"{count}_{ele.word}"] = ele
                            self.vocab.add(ele.word)
                            count += 1
                logger.info("Load glossary file successfully!")
            except Exception as e:
                logger.error("Function load_glossary has errors!")
                logger.error(e)
                return False
        return True

    def getSememeByID(self, id: int):
        """根据编号获取义原"""
        if id in self.sememe_table:
            return self.sememe_table[id]
        return None

    def getSememeByWord(self, word: str):
        """根据单词获取义原"""
        if word in self.sememeindex_zh:
            return self.sememeindex_zh[word]
        return None

    @lru_cache(maxsize=64)
    def getGlossaryByWord(self, word: str):
        """根据单词获取词汇表中的项"""
        if word in self.vocab:
            return valuesOfGlossaryTable(self.glossary_table, word)
        return None

    def weight(self, index: int):
        left = 1 - index / 13
        right = 1 + math.sin(index * math.pi / 45)
        return left * right

    def calcSememeDistance(self, w1: str, w2: str):
        """计算义原之间的距离（即义原树中两个节点之间的距离）"""
        s1 = self.getSememeByWord(w1)
        s2 = self.getSememeByWord(w2)

        if s1 is None or s2 is None:
            return -1.0

        father_path = []

        id1, id2 = s1.id, s2.id
        father1, father2 = s1.father, s2.father

        # 追溯s1的上位词
        while (id1 != father1):
            father_path.append(id1)
            id1 = father1
            father_ = self.getSememeByID(father1)
            if father_:
                father1 = father_.father

        father_path.append(id1)
        # 计算距离的权重
        len_ = 0.0
        while (id2 != father2):
            if id2 in father_path:
                father_pos = father_path.index(id2)
                return self.weight(father_pos) + len_

            id2 = father2
            father_ = self.getSememeByID(father2)
            if father_:
                father2 = father_.father
            len_ = len_ + self.weight(1)

        if id2 in father_path:
            father_pos = father_path.index(id2)
            return self.weight(father_pos) + len_
        return 20.0

    def calcSememeSim(self, w1: str, w2: str):
        """计算两个单词在义原树上的相似度"""
        if not w1 and not w2:
            return 1.0
        if not w1 or not w2:
            return self.DELTA
        if w1 == w2:
            return 1.0

        d = self.calcSememeDistance(w1, w2)
        if d >= 0:
            return self.ALFA / (self.ALFA + d)
        else:
            return -1.0

    def calcSememeSimFirst(self, g1: GlossaryElement, g2: GlossaryElement):
        """计算第一基本义原之间的相似度"""
        return self.calcSememeSim(g1.s_first, g2.s_first)

    def calcSememeSimOther(self, g1: GlossaryElement, g2: GlossaryElement):
        """计算其他独立义原之间的相似度"""
        if len(g1.s_other) <= 0 and len(g2.s_other) <= 0:
            return 1.0
        sum_ = 0.0
        for i in range(len(g1.s_other)):
            maxTemp = -1.0

            for j in range(len(g2.s_other)):
                temp = 0.0
                if g1.s_other[i][0] != "(" and g2.s_other[j][0] != "(":
                    temp = self.calcSememeSim(g1.s_other[i], g2.s_other[j])
                elif g1.s_other[i][0] == "(" and g2.s_other[j][0] == "(":
                    if g1.s_other[i] == g2.s_other[j]:
                        temp = 1.0
                    else:
                        maxTemp = 0.0
                else:
                    temp = self.GAMA

                if temp > maxTemp:
                    maxTemp = temp

            if maxTemp == -1.0:
                maxTemp = self.DELTA

            sum_ += maxTemp

        sum_ += abs(len(g1.s_other) - len(g2.s_other)) * self.DELTA
        return sum_ / max(len(g1.s_other), len(g2.s_other))

    def calcSememeSimRelation(self, g1: GlossaryElement, g2: GlossaryElement):
        """计算关系义原之间的相似度"""
        if len(g1.s_relation) <= 0 and len(g2.s_relation) <= 0:
            return 1.0

        sum_ = 0.0
        for it1 in g1.s_relation:
            maxTemp = 0.0
            temp = 0.0

            if it1 in g2.s_relation:
                if g1.s_relation[it1][0] != "(" and g2.s_relation[it1][0] != "(":
                    temp = self.calcSememeSim(g1.s_relation[it1], g2.s_relation[it1])
                elif g1.s_relation[it1][0] == "(" and g2.s_relation[it1][0] == "(":
                    if g1.s_relation[it1] == g2.s_relation[it1]:
                        temp = 1.0
                    else:
                        maxTemp = 0.0
                else:
                    temp = self.GAMA
            else:
                maxTemp = self.DELTA

            if temp > maxTemp:
                maxTemp = temp

            sum_ += maxTemp

        sum_ += abs(len(g1.s_relation) - len(g2.s_relation)) * self.DELTA
        return sum_ / max(len(g1.s_relation), len(g2.s_relation))

    def calcSememeSimSymbol(self, g1: GlossaryElement, g2: GlossaryElement):
        """计算符号义原之间的相似度"""
        if len(g1.s_symbol) <= 0 and len(g2.s_symbol) <= 0:
            return 1.0

        sum_ = 0.0
        for it1 in g1.s_symbol:
            maxTemp = 0.0
            temp = 0.0

            if it1 in g2.s_symbol:
                if g1.s_symbol[it1][0] != "(" and g2.s_symbol[it1][0] != "(":
                    temp = self.calcSememeSim(g1.s_symbol[it1], g2.s_symbol[it1])
                elif g1.s_symbol[it1][0] == "(" and g2.s_symbol[it1][0] == "(":
                    if g1.s_symbol[it1] == g2.s_symbol[it1]:
                        temp = 1.0
                    else:
                        maxTemp = 0.0
                else:
                    temp = self.GAMA
            else:
                maxTemp = self.DELTA
            if temp > maxTemp:
                maxTemp = temp

            sum_ += maxTemp

        sum_ += abs(len(g1.s_symbol) - len(g2.s_symbol)) * self.DELTA
        return sum_ / max(len(g1.s_symbol), len(g2.s_symbol))

    def calcGlossarySim(self, g1: GlossaryElement, g2: GlossaryElement):
        """计算词汇表中两个单词的相似度"""
        if g1 is None or g2 is None:
            return 0.0

        if g1.solid != g2.solid:
            return 0.0

        sim1 = self.calcSememeSimFirst(g1, g2)
        sim2 = self.calcSememeSimOther(g1, g2)
        sim3 = self.calcSememeSimRelation(g1, g2)
        sim4 = self.calcSememeSimSymbol(g1, g2)

        sim = self.BETA[0] * sim1 + self.BETA[1] * sim1 * sim2 + self.BETA[2] * sim1 * sim2 * sim3 + \
            self.BETA[3] * sim1 * sim2 * sim3 * sim4
        return sim

    def word_sim(self, w1: str, w2: str) -> float:
        """
        计算两个单词的语义相似度 （返回值再0-1之间，-1表示有单词在词典中不存在）
        """
        if w1 == w2:
            return 1.0

        g1_list = self.getGlossaryByWord(w1)
        g2_list = self.getGlossaryByWord(w2)

        if g1_list is None or g2_list is None or len(g1_list) <= 0 or len(g2_list) <= 0:
            return -1.0

        max_ = 0.0
        for i in range(len(g1_list)):
            for j in range(len(g2_list)):
                tmp = self.calcGlossarySim(g1_list[i], g2_list[j])
                max_ = max(max_, tmp)

        return max_

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
    glossary_file = "../../data/resources/glossary.txt"
    sememe_file = "../../data/resources/WHOLE.DAT"

    # 初始化
    hownet = HowNetSimilarity(glossary_file, sememe_file)

    print(hownet.word_sim("开心", "难过"))