# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-03
from typing import Dict, List, Union, Tuple
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from gensim.models.word2vec import Word2VecKeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

from novela import logger


logger = logger.getChild("word2vector")


class WordVectorSimilarity:
    def __init__(self, w2v_file: str,
                 word2vec: Union[Word2VecKeyedVectors, Dict[str, np.ndarray]] = None):
        if w2v_file is None and word2vec is None:
            raise ValueError(f"`w2v_file` and `word2vec` can both be None.")
        # 是否提供了词向量对象
        if word2vec is not None:
            self.word2vec = word2vec
            if isinstance(word2vec, Word2VecKeyedVectors):
                self.vocab_size = len(self.word2vec.vocab)
                self.vector_size = self.word2vec.vector_size
            else:
                self.vocab_size = len(self.word2vec)
                self.vector_size = len(self.word2vec[list(self.word2vec.keys())[0]])
        else:
            # 加载词向量
            self._load_wordvectors(w2v_file)
        logger.info(f"加载了词向量共包含单词{self.vocab_size}个，词向量长度为{self.vector_size}。")

    def _load_wordvectors(self, w2v_file: str):
        try:
            self.word2vec = KeyedVectors.load_word2vec_format(w2v_file)
            self.vocab_size = len(self.word2vec.vocab)
            self.vector_size = self.word2vec.vector_size
        except Exception as e:
            logger.warning(f"使用gensim加载词向量出错!@{e}")
            word2vec_dict: Dict[str, np.ndarray] = {}
            vector_size = 0
            with open(w2v_file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    # 防止第一行是表示词表大小和向量大小的标志
                    if i == 0:
                        line_list = line.split()
                        if len(line_list) == 2:
                            vector_size = int(line_list[1])
                            continue
                    # 如果不是则继续读取
                    # 这里得到的vector_string是str型，只不过每个float数字之间用空格分割
                    word, vector_string = line.split(" ", 1)
                    word2vec_dict[word] = np.fromstring(vector_string, dtype=float, sep=" ")
                    if vector_size == 0:
                        vector_size = len(word2vec_dict[word])
            # 最终得到单词到词向量的映射
            self.word2vec = word2vec_dict
            self.vocab_size = len(word2vec_dict)
            self.vector_size = vector_size

    def _get_matrix_and_mask(self, word_list: List[str]):
        word_matrix, word_mask = [], []
        for word in word_list:
            try:
                vec = self.word2vec[word]
                word_matrix.append(vec)
                word_mask.append(1.0)
            except:
                logger.error(f"单词{word}不存在于词向量词表中！")
                word_matrix.append(np.zeros(self.vector_size))
                word_mask.append(0.0)
        word_matrix = np.asarray(word_matrix)
        word_mask = np.asarray(word_mask)
        return word_matrix, word_mask

    def vector_cosine_sim(self, vec_a: np.ndarray, vec_b: np.ndarray):
        # norm默认是2范数
        cosine_sim = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        return cosine_sim

    def word_sim(self, w1: str, w2: str) -> float:
        if w1 == w2:
            return 1.0
        # 获取单词的词向量
        try:
            w1_vec = self.word2vec[w1]
        except:
            logger.error(f"{w1}不存在于词向量词表中！")
            return -1.0

        try:
            w2_vec = self.word2vec[w2]
        except:
            logger.error(f"{w2}不存在于词向量词表中！")
            return -1.0

        cosine_sim = self.vector_cosine_sim(w1_vec, w2_vec)
        # 由于cosine_sim的范围在[-1, 1]之间
        # 这里将其归一化到[0, 1]之间
        norm_cosine_sim = (cosine_sim + 1) / 2

        return norm_cosine_sim

    def wordlist_sim(self, word_list1: List[str], word_list2: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        # 如果两个列表相等
        if word_list1 == word_list2:
            word_list_sim = np.ones(shape=(len(word_list1), len(word_list2)),
                                    dtype=float)

            return word_list_sim, word_list_sim

        # 否则计算两个列表中每一个单词的相似度
        # 首先获取两个单词列表的词向量矩阵
        word_list1_matrix, word_list1_mask = self._get_matrix_and_mask(word_list1)
        word_list2_matrix, word_list2_mask = self._get_matrix_and_mask(word_list2)

        # 使用cosine_similarity计算相似度
        # 维度为 word_list1_len * word_list2_len
        similarities = cosine_similarity(word_list1_matrix, word_list2_matrix)

        # 余弦相似度范围在[-1, 1]之间，这里归一化到[0, 1]之间
        similarities = (similarities + 1) / 2

        w1_expand = np.expand_dims(word_list1_mask, axis=1)
        w2_expand = np.expand_dims(word_list2_mask, axis=0)
        masks = (w1_expand & w2_expand)

        # 分别乘以word_list1和word_list2的mask向量
        similarities = similarities * masks

        return similarities, masks



