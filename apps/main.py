# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-26
import os
import base64
import io
from flask import Flask
from flask import render_template, request
from flask.views import View

from apps.outline_funcs import *
from novela import logger
from novela.utils.common import get_wordcloud
import novela.constants as constants



logger = logger.getChild("outline-app")


app = Flask(__name__,
            template_folder="../novel_frontend/dist",
            static_folder="../novel_frontend/dist/static")


class OutlineApp():
    def __init__(self):
        self.sim_word2vector = None
        self.sim_cilin = None
        self.sim_hownet = None
        self.sim_sent2vector = None
        self.stopwords = set()

    # @app.route('/')
    # @app.route('/index')
    def index(self):
        return render_template('index.html')

    # @app.route('/init', methods=["POST"])
    def init_model(self):
        logger.info("开始初始化模型")
        start_time = time.time()
        params = request.json
        word2vec_file = params.get("word2vec_file")
        # 加载停用词
        self.stopwords = load_stopwords(file=constants.STOPWORDS_FILE)
        # --- 单词相似度部分 ---
        logger.info("构造单词语义相似度计算对象")
        self.sim_word2vector = WordVectorSimilarity(w2v_file=word2vec_file)
        logger.info("构造词林相似度对象")
        self.sim_cilin = CilinSimilarity(cilin_file=constants.CILIN_FILE)
        logger.info("构造HowNet相似度计算对象")
        self.sim_hownet = HowNetSimilarity(glossary_file=constants.GLOSSARY_FILE,
                                      sememe_file=constants.WHOLE_DAT)
        # --- 语句相似度部分 ---
        logger.info("构造语句相似度计算对象")
        self.sim_sent2vector = SentVectorSimilarity(stopwords=self.stopwords,
                                               word2vec=self.sim_word2vector.word2vec)

        logger.info(f"初始化共计用时 {time.time() - start_time} s.")
        return {"message": "初始化成功", "status_code": 1}

    # @app.route('/analysis', methods=["POST"])
    def analysis(self):
        params = request.json
        source_path = params.get("source_path")
        source_file = params.get("source_file")
        target_path = params.get("target_path")
        target_file = params.get("target_file")

        # 首先判断文件夹和文件是否存在
        if not os.path.isdir(source_path):
            raise RuntimeError(f"The parameter `source_dir`: {source_path} is not a valid path.")

        source_file = os.path.join(source_path, source_file)
        if not os.path.isfile(source_file):
            raise ValueError(f"There is no file named `source_file`: {source_file}.")

        # 判断目标文件目录是否存在
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
        target_file = os.path.join(target_path, target_file)

        # 将文件中的数据转化为Dict型
        logger.info(f"读取小说大纲文件{source_file}，并转化为Comic对象")
        document_dict = read_document_to_dict(file=source_file)
        novel_name = document_dict["小说名"]  # 小说的名称
        # 转化为Comic对象
        comic = Comic()
        parse_document(document_dict, comic=comic)

        # 获取整个story中的strings和words
        story_sent_strings, story_sent_words, words_tfidf, *_ = get_story_words_and_sentences(comic,
                                                                                              self.stopwords)
        wordcloud_img = self.get_tfidf_wordcloud(sent_words=story_sent_words,
                                                 words_tfidf=words_tfidf)

        # 创建空的Label对象
        label = Label()

        start_time = time.time()
        classify_base_info(comic=comic, label=label)
        logger.info(f"得到基本信息的标签，共计用时 {(time.time() - start_time) * 1000} ms.")

        start_time = time.time()
        classify_story_info(comic=comic, label=label,
                            stopwords=self.stopwords,
                            sim_word2vector=self.sim_word2vector,
                            sim_cilin=self.sim_cilin,
                            sim_hownet=self.sim_hownet,
                            sim_sent2vector=self.sim_sent2vector,
                            sent_words=story_sent_words,
                            sent_strings=story_sent_strings)
        logger.info(f"得到故事信息的标签，共计用时 {(time.time() - start_time) * 1000} ms.")

        start_time = time.time()
        classify_role_info(comic=comic, label=label,
                           stopwords=self.stopwords,
                           sim_word2vector=self.sim_word2vector,
                           sim_cilin=self.sim_cilin,
                           sim_hownet=self.sim_hownet,
                           sim_sent2vector=self.sim_sent2vector)
        logger.info(f"得到角色信息的标签，共计用时 {(time.time() - start_time) * 1000} ms.")

        start_time = time.time()
        classify_other_info(comic=comic, label=label,
                            stopwords=self.stopwords,
                            sim_word2vector=self.sim_word2vector,
                            sim_cilin=self.sim_cilin,
                            sim_hownet=self.sim_hownet,
                            sim_sent2vector=self.sim_sent2vector,
                            sent_words=story_sent_words,
                            sent_strings=story_sent_strings)
        logger.info(f"得到其他信息的标签，共计用时 {(time.time() - start_time) * 1000} ms.")

        logger.info(f"保存文件到{target_file}")
        save_as_excel(to_file=target_file,
                      novel_name=novel_name,
                      label=label)
        logger.info("保存完成！")

        return wordcloud_img

    def get_tfidf_wordcloud(self,
                            sent_words: List[str],
                            words_tfidf: List[float]):
        wc = get_wordcloud(font_path=constants.FONT_FILE,
                           width=800,
                           height=400,
                           max_font_size=300,
                           max_words=80,
                           background_color="white")
        data = dict(zip(sent_words, words_tfidf))
        pil_img = wc.generate_from_frequencies(data).to_image()
        img = io.BytesIO()
        pil_img.save(img, 'PNG')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        return img_base64



