# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-20
from typing import List


class Outline(object):
    def __init__(self,
                 title: str = "",
                 novel_author: str = "",
                 comic_author: str = "",
                 novel_type: List[str] = None,
                 target_user_start: float = 0.0,
                 target_user_end: float = float("inf"),
                 features: List[str] = None,
                 background: str = "",
                 summarization: str = ""):
        """
        定义作品的大纲
        :param title: str型，表示作品的名称
        :param novel_author: str型，表示小说的作者
        :param comic_author: str型，表示漫画的作者
        :param novel_type: List[str]型，表示漫画/小说的类型
        :param target_user_start: float型，表示漫画/小说的目标受众的起始年龄
        :param target_user_end: float型，表示漫画/小说的目标受众的结束年龄
        :param features: List[str]型，表示小说的一些特点，可能包含多句话
        :param background: str型，表示小说发生的背景
        :param summarization: str型，表示小说的梗概
        """
        if target_user_start < 0 or target_user_end < 0:
            raise ValueError("target user's age can't lower than 0.")
        self._title = title
        self._novel_author = novel_author
        self._comic_author = comic_author
        self._novel_type = novel_type
        self._target_user_start = target_user_start
        self._target_user_end = target_user_end
        self._features = features
        self._background = background
        self._summarization = summarization

    def add_info_to_outline(self, **kwargs):
        title = kwargs.get("title", None)
        novel_author = kwargs.get("novel_author", None)
        comic_author = kwargs.get("comic_author", None)
        if title is not None:
            self._title = title
        if novel_author is not None:
            self._novel_author = novel_author
        if comic_author is not None:
            self._comic_author = comic_author

        if "novel_type" in kwargs:
            self._novel_type = kwargs.get("novel_type")
        if "target_user_start" in kwargs:
            self._target_user_start = kwargs.get("target_user_start")
        if "target_user_end" in kwargs:
            self._target_user_end = kwargs.get("target_user_end")
        if "features" in kwargs:
            self._features = kwargs.get("features")
        if "background" in kwargs:
            self._background = kwargs.get("background")
        if "summarization" in kwargs:
            self._summarization = kwargs.get("summarization")

    @property
    def title(self):
        return self._title

    @property
    def novel_author(self):
        return self._novel_author

    @property
    def comic_author(self):
        return self._comic_author

    @property
    def novel_type(self):
        return self._novel_type

    @property
    def target_user_start(self):
        return self._target_user_start

    @property
    def target_user_end(self):
        return self._target_user_end

    @property
    def features(self):
        return self._features

    @property
    def background(self):
        return self._background

    @property
    def summarization(self):
        return self._summarization

    @title.setter
    def title(self, t: str):
        self._title = t

    @novel_author.setter
    def novel_author(self, na: str):
        self._novel_author = na

    @comic_author.setter
    def comic_author(self, ca: str):
        self._comic_author = ca

    @novel_type.setter
    def novel_type(self, nt: List[str]):
        self._novel_type = nt

    @target_user_start.setter
    def target_user_start(self, tus: float):
        self._target_user_start = tus

    @target_user_end.setter
    def target_user_end(self, tue: float):
        self._target_user_end = tue

    @features.setter
    def features(self, f: List[str]):
        self._features = f

    @background.setter
    def background(self, bg: str):
        self._background = bg

    @summarization.setter
    def summarization(self, sm: str):
        self._summarization = sm
