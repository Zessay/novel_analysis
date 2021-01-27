# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-20
from typing import List, Optional, Union


class Person(object):
    def __init__(self,
                 name: str = "",
                 nick_name: Union[str, List[str]] = "",
                 appearance: str = "",
                 age: float = 0,
                 gender: str = "",
                 desire: str = "",
                 interest: Optional[List[str]] = None,
                 speciality: Optional[List[str]] = None,
                 character: Optional[List[str]] = None,
                 weakness: Optional[List[str]] = None):
        """
        定义一个作品中的人物
        :param name: str型，表示人物的名字
        :param nick_name: str型或者List[str]，表示人物的昵称
        :param appearance: str型，表示人物外貌特征
        :param age: int型，表示人物的年龄
        :param gender: str型，表示人物的性别
        :param desire: str型，表示人物的欲求
        :param interest: List[str]，表示人物的兴趣
        :param speciality: List[str]，表示人物的特长
        :param character: List[str]，表示人物的性格
        :param weakness: List[str]，表示人物的缺点
        """
        if age < 0:
            raise ValueError("age can't lower than 0.")
        self._name = name
        self._nick_name = nick_name
        self._appearance = appearance
        self._age = age
        self._gender = gender
        self._desire = desire
        self._interest = interest
        self._speciality = speciality
        self._character = character
        self._weakness = weakness
        self.dialog_sents = {}     # 表示该人物所说的话，元素是键值对的形式，键表示该句话出现的章节(int)，值表示该人物该章节说话的内容(List[str])
        self.include_sents = {}    # 表示不属于该人物所说的话，但是包含该人物名字的语句，元素同上

    def add_sent2dialog(self, sent: str, chapter: int = 0):
        if chapter in self.dialog_sents:
            self.dialog_sents[chapter].append(sent)
        else:
            self.dialog_sents[chapter] = [sent]

    def add_sent2include(self, sent: str, chapter: int = 0):
        if chapter in self.include_sents:
            self.include_sents[chapter].append(sent)
        else:
            self.include_sents[chapter] = [sent]

    def add_sents2dialog(self, sents: List[str], chapter: int = 0):
        if chapter in self.dialog_sents:
            self.dialog_sents[chapter].extend(sents)
        else:
            self.dialog_sents[chapter] = sents

    def add_sents2include(self, sents: List[str], chapter: int = 0):
        if chapter in self.include_sents:
            self.include_sents[chapter].extend(sents)
        else:
            self.include_sents[chapter] = sents

    @property
    def name(self):
        return self._name

    @property
    def nick_name(self):
        return self._nick_name

    @property
    def appearance(self):
        return self._appearance

    @property
    def age(self):
        return self._age

    @property
    def gender(self):
        return self._gender

    @property
    def desire(self):
        return self._desire

    @property
    def interest(self):
        return self._interest

    @property
    def speciality(self):
        return self._speciality

    @property
    def character(self):
        return self._character

    @property
    def weakness(self):
        return self._weakness

    @name.setter
    def name(self, n: str):
        self._name = n

    @nick_name.setter
    def nick_name(self, nn: Union[str, List[str]]):
        self._nick_name = nn

    @appearance.setter
    def appearance(self, appear: str):
        self._appearance = appear

    @age.setter
    def age(self, a: float):
        if a < 0:
            raise ValueError("age can't lower than 0.")
        self._age = a

    @gender.setter
    def gender(self, g: str):
        self._gender = g

    @desire.setter
    def desire(self, d: str):
        self._desire = d

    @interest.setter
    def interest(self, i: List[str]):
        self._interest = i

    @speciality.setter
    def speciality(self, s: List[str]):
        self._speciality = s

    @character.setter
    def character(self, c: List[str]):
        self._character = c

    @weakness.setter
    def weakness(self, w: List[str]):
        self._weakness = w
