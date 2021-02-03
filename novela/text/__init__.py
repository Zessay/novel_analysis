# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-27
from novela.text.sim_cilin import CilinSimilarity
from novela.text.sim_hownet import HowNetSimilarity
from novela.text.sim_word2vec import WordVectorSimilarity
from novela.text.sentsim_word2vec import SentVectorSimilarity


__all__ = ["CilinSimilarity", "HowNetSimilarity", "WordVectorSimilarity", "SentVectorSimilarity"]