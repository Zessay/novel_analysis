# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-03
from gensim.models.keyedvectors import KeyedVectors


if __name__ == '__main__':
    # w2v_file = "../data/resources/sgns.literature.word.bz2"
    w2v_file = "../data/resources/w2v_sample.txt"
    word2vec = KeyedVectors.load_word2vec_format(w2v_file)

    print(len(word2vec.vocab))
    print(word2vec.vector_size)
    print(type(word2vec["的"]))