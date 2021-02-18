# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-03
import jieba
from typing import Union, Dict, List, Optional, Tuple, Set
import numpy as np
from gensim.models.word2vec import Word2VecKeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

from novela import logger
from novela.utils.common import load_stopwords
from novela.text.sim_word2vec import WordVectorSimilarity


logger = logger.getChild("sentvector")


class SentVectorSimilarity(WordVectorSimilarity):
    def __init__(self,
                 w2v_file: str = None,
                 stopwords: Optional[Union[str, Set[str]]] = None,
                 word2vec: Union[Word2VecKeyedVectors, Dict[str, np.ndarray]] = None):
        super().__init__(w2v_file, word2vec)

        if stopwords is None:
            self.stopwords = []
        elif isinstance(stopwords, set):
            self.stopwords = stopwords
        else:
            self.stopwords = load_stopwords(stopwords)

    def _get_sent_vector(self, sent: Union[str, List[str]]):
        # 如果是str型则要进行分词
        if isinstance(sent, str):
            sent = jieba.lcut(sent)

        sent_vector = np.zeros(self.vector_size)
        valid = 0
        for word in sent:
            if word not in self.stopwords:
                try:
                    vec = self.word2vec[word]
                    sent_vector += vec
                    valid += 1
                except:
                    pass
        # 对词向量的和进行平均
        # 得到句向量
        sent_vector /= valid
        return sent_vector, valid

    def _get_matrix_and_mask(self, sent_list: Union[List[str], List[List[str]]]):
        sent_matrix, sent_mask = [], []
        for sent in sent_list:
            sent_vector, sent_valid = self._get_sent_vector(sent)
            if sent_valid:
                sent_mask.append(1.0)
            else:
                sent_mask.append(0.0)
            sent_matrix.append(sent_vector)
        sent_matrix = np.asarray(sent_matrix)
        sent_mask = np.asarray(sent_mask)
        return sent_matrix, sent_mask

    def sent_sim(self, sent1: Union[str, List[str]], sent2: Union[str, List[str]]) -> float:
        if sent1 == sent2:
            return 1.0

        sent1_vector, sent1_valid = self._get_sent_vector(sent1)
        sent2_vector, sent2_valid = self._get_sent_vector(sent2)

        # 如果有一个句子不存在有效单词
        if sent1_valid == 0 or sent2_valid == 0:
            return -1.0

        cosine_sim = self.vector_cosine_sim(sent1_vector, sent2_vector)
        # 由于余弦相似度的范围是[-1, 1]
        # 这里归一化到[0, 1]之间
        cosine_sim = (cosine_sim + 1) / 2

        return cosine_sim

    def sentlist_sim(self,
                     sent_list1: Union[List[str], List[List[str]]],
                     sent_list2: Union[List[str], List[List[str]]]) -> Tuple[np.ndarray, np.ndarray]:

        # 首先获取两个句子列表中每一个句子的句向量
        # 以及对应的mask向量
        sent_list1_matrix, sent_list1_mask = self._get_matrix_and_mask(sent_list1)
        sent_list2_matrix, sent_list2_mask = self._get_matrix_and_mask(sent_list2)

        # 使用cosine_similarity计算相似度
        similarities = cosine_similarity(sent_list1_matrix, sent_list2_matrix)

        # 余弦相似度的范围在[-1, 1]之间，这里归一化到[0, 1]之间
        similarities = (similarities + 1) / 2

        s1_expand = np.expand_dims(sent_list1_mask, axis=1)
        s2_expand = np.expand_dims(sent_list2_mask, axis=0)
        masks = (s1_expand & s2_expand)

        similarities = similarities * masks
        return similarities, masks
