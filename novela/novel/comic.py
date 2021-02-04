# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-04
from typing import List, Tuple, Dict
from typing import Union, Optional, Any
from dataclasses import dataclass

from novela import logger
from novela.novel.person import Person
from novela.novel.outline import Outline
from novela.novel.story_line import StoryLine


logger = logger.getChild("comic")


@dataclass
class Sentence:
    """
    表示一句话，可能是人物的对话、内心独白，或者是旁白
    """
    speaker: str = None           # 表示说话人的名字
    sentence: str = None          # 表示说话的内容


@dataclass
class Section:
    """
    表示漫画/小说中的一个章节
    """
    section_id: int = -1                 # 表示该章节属于哪一话
    title: str = None                    # 表示章节的标题
    sentences: List[Sentence] = None     # 表示该章节中的语句



class Comic:
    def __init__(self, name: str = None):
        self._name = name                                   # 表示小说/漫画的名称
        self.sections: List[Section] = []                   # 表示该小说/漫画的所有章节
        self.first_role: Person = None                      # 表示该小说的第一主角
        self.second_role: Person = None                     # 表示该小说的第二主角
        self.other_roles: List[Person] = []                 # 表示小说的其他角色
        self.relations: List[Tuple[str, str, str]] = []     # 表示小说中存在的人物关系，每一个元素是一个三元组(head, relation, tail)

        self.outline: Outline = None                        # 表示漫画的大纲
        self.storyline: StoryLine = None                    # 表示整个故事的起承转合

        # 将所有角色放到一个列表中便于索引
        self.roles = [self.first_role, self.second_role] + self.other_roles

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n: str):
        self._name = n

    def _inspect_section(self, section_id: int):
        """
        表示根据section_id检查当前sections的数量
        :param section_id:
        :return:
        """
        if section_id < 0:
            raise ValueError(f"Section ID must be equal or greater than 0, while get `{section_id}`")
        section_length = len(self.sections)
        if section_id < section_length:
            pass
        elif section_id == section_length:
            self.sections.append(None)
        else:
            none_section_num = section_id - section_length + 1
            self.sections += ([None] * none_section_num)

    def _inspect_relation_triplets(self, relation: Tuple[str, str, str]):
        if not isinstance(relation, tuple):
            raise TypeError(f"The relation triplets should be `tuple` type, while get `{type(relation)}`!")
        if len(relation) != 3:
            raise IndexError(f"The relation triplets should have three elements, namely (`head`,`relation`, `tail`), "
                             f"while the accepted `relation`'s length is `{len(relation)}`!")
        if not (isinstance(relation[0], str) and isinstance(relation[1], str) and isinstance(relation[2], str)):
            raise TypeError(f"We hope that the elements of `relation` are `str` type, while `head`/`relation`/`tail` "
                            f"is respectively `{type(relation[0])}`/`{type(relation[1])}`/`{type(relation[2])}`!")

    def add_section(self, section: Section):
        """
        添加一个章节
        :param section:
        :return:
        """
        # 获取当前章节的id
        section_id = section.section_id
        self._inspect_section(section_id)
        self.sections[section_id] = section

    def add_sections(self, sections: List[Section]):
        """
        添加多个章节
        :param sections:
        :return:
        """
        # 将每一个章节逐个添加进去
        for section in sections:
            self.add_section(section)

    def add_sentence_to_section(self,
                                sentence: Union[Sentence, Tuple[str, str]],
                                section_id: int,
                                title: Optional[str] = None):
        """
        将一个句子添加到某个章节中
        :param sentence: 这里的sentence要么是Sentence对象；要么是Tuple[str, str]，第一个str表示说话人，第二个str表示说话内容
        :param section_id: int型，表示需要添加到的章节id
        :param title: str型，可选参数，如果已知当前章节原来没有出现，最好指定标题创建新的对象
        :return:
        """
        if sentence is None:
            return
        # 首先检查当前的sections是否能够满足section_id的需求
        self._inspect_section(section_id)
        # 如果当前的section_id对应的位置是None，则需要新建一个Section对象
        if self.sections[section_id] is None:
            self.sections[section_id] = Section(section_id=section_id, title=title)

        if isinstance(sentence, tuple):
            # 根据Tuple的内容创建Sentence对象
            sentence_obj = Sentence(speaker=sentence[0], sentence=sentence[1])
            sentence = sentence_obj

        self.sections[section_id].sentences.append(sentence)

    def add_sentences_to_section(self,
                                 sentences: Union[List[Sentence], List[Tuple[str, str]]],
                                 section_id: int,
                                 title: Optional[str] = None):
        """
        将多个句子添加到一个章节中
        """
        if len(sentences) <= 0:
            return
        for sentence in sentences:
            self.add_sentence_to_section(sentence, section_id, title)

    def add_sentences_to_sections(self,
                                  contents: List[Dict[str, Any]]):
        """
        将多个句子添加到多个章节中
        :param contents: 这里的contents是一个list型，每一个元素是一个dict，包含一个章节以及其需要添加的句子
                         至少应该包含`section_id`字段以及`sentences`字段，`title`字段可选
        :return:
        """
        if len(contents) <= 0:
            return
        section_count = 0
        sentence_count = 0
        for i, content in enumerate(contents):
            if ("section_id" in content) and ("sentences" in content):
                section_id = content["section_id"]
                sentences = content["sentences"]
                title = None if "title" not in content else content["title"]
                self.add_sentences_to_section(sentences=sentences,
                                              section_id=section_id,
                                              title=title)
                section_count += 1
                sentence_count += len(sentences)
            else:
                logger.warning(f"第{i}个元素当前内容的键中{content.keys()}不同时包含`section_id`和`sentences`！！！")

        logger.info(f"共计添加了{sentence_count}个句子到{section_count}个章节中！")

    def add_new_role(self, role: Person, whether_exist: bool = True, replace: bool = True):
        """
        向other roles中添加新的角色
        :param role: Person类型，表示新角色
        :param whether_exist: bool型，表示是否需要判断该角色存在与否
        :param replace: bool型，如果存在该角色是否替换
        :return:
        """
        exist = False
        if whether_exist:
            for i, r in enumerate(self.roles):
                if r is not None:
                    if r.name == role.name:
                        exist = True
                        if replace:
                            self.roles[i] = role
                            self.other_roles[i-2] = role
                        break
        # 如果没有存在，则添加到Other roles和roles中
        if not exist:
            self.other_roles.append(role)
            self.roles.append(role)

    def get_role_according_name(self, role_name: str) -> Person:
        """根据角色名字获取角色对象"""
        # 遍历已有的角色列表
        for role in self.roles:
            if role is not None:
                if role.name == role_name:
                    return role

        # 如果遍历完所有的角色仍然没有找到，则创建该角色
        role = Person(name=role_name)
        self.add_new_role(role, whether_exist=False)
        return role

    def _add_info_to_role(self, role: Person, **kwargs):
        if role is None:
            return
        if len(kwargs) <= 0:
            return
        # 向该人物中添加一些信息
        role.add_info_to_person(**kwargs)

    def add_info_to_first_role(self, **kwargs):
        """添加第一主角的角色信息"""
        if self.first_role is None:
            self.first_role = Person()
        self._add_info_to_role(self.first_role, **kwargs)

    def add_info_to_second_role(self, **kwargs):
        """添加第二主角的角色信息"""
        if self.second_role is None:
            self.second_role = Person()
        self._add_info_to_role(self.second_role, **kwargs)

    def add_info_to_role(self, role_name: str, **kwargs):
        """可以根据名字向任何角色中添加信息"""
        # 首先根据名字获取该角色对象
        role = self.get_role_according_name(role_name)
        self._add_info_to_role(role, **kwargs)

    def add_relations(self, relations: Union[Tuple[str, str, str], List[Tuple[str, str, str]]]):
        """向关系三元组中添加关系"""
        if relations is None:
            return
        if isinstance(relations, tuple):
            # 首先检查relations的类型是否正确
            self._inspect_relation_triplets(relations)
            self.relations.append(relations)
        elif isinstance(relations, list):
            for ele in relations:
                self._inspect_relation_triplets(ele)
                self.relations.append(ele)
        else:
            raise TypeError(f"Only `tuple` or `List[tuple]` can be recognized, while get `{type(relations)}` type.")

    def add_outline(self, outline: Optional[Outline] = None, **kwargs):
        """向漫画类中添加一个大纲Outline，或者向已有的Outline中添加一些信息"""
        if outline is not None:
            self.outline = outline
        else:
            if self.outline is None:
                self.outline = Outline()
            self.outline.add_info_to_outline(**kwargs)

    def add_storyline(self, storyline: Optional[StoryLine] = None, **kwargs):
        """向漫画类中添加一个故事剧情走向属性Storyline，或者向已有的Storyline中添加一些信息"""
        if storyline is not None:
            self.storyline = storyline
        else:
            if self.storyline is None:
                self.storyline = StoryLine()
            self.storyline.add_info_to_storyline(**kwargs)

    def _add_dialog_sentence_to_role(self,
                                     role: Person,
                                     sents: Optional[Union[str, List[str]]] = None,
                                     section: int = 0,
                                     sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):

        if sents is None and sents_dict is None:
            logger.warning(f"No dialog sentences added to {role.name} at this time.")
            return
        if sents is not None:
            if isinstance(sents, str):
                role.add_sent2dialog(sents, section)
            elif isinstance(sents, list):
                role.add_sents2dialog(sents, section)
            else:
                raise TypeError(f"Only `str` or `List[str]` can be accepted, while get `{type(sents)}`.")
        else:
            # key表示章节，是int型；value表示该章节对应的句子内容
            for key, value in sents_dict.items():
                if isinstance(value, str):
                    role.add_sent2dialog(value, key)
                elif isinstance(value, list):
                    role.add_sents2dialog(value, key)
                else:
                    raise TypeError(f"Only `str` or `List[str]` can be accepted, while get `{type(value)}`.")

    def _add_include_sentence_to_role(self,
                                      role: Person,
                                      sents: Optional[Union[str, List[str]]] = None,
                                      section: int = 0,
                                      sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):

        if sents is None and sents_dict is None:
            logger.warning(f"No dialog sentences added to {role.name} at this time.")
            return
        if sents is not None:
            if isinstance(sents, str):
                role.add_sent2include(sents, section)
            elif isinstance(sents, list):
                role.add_sents2include(sents, section)
            else:
                raise TypeError(f"Only `str` or `List[str]` can be accepted, while get `{type(sents)}`.")
        else:
            # key表示章节，是int型；value表示该章节对应的句子内容
            for key, value in sents_dict.items():
                if isinstance(value, str):
                    role.add_sent2include(value, key)
                elif isinstance(value, list):
                    role.add_sents2include(value, key)
                else:
                    raise TypeError(f"Only `str` or `List[str]` can be accepted, while get `{type(value)}`.")

    def add_dialog_sentence_to_first_role(self,
                                          sents: Optional[Union[str, List[str]]] = None,
                                          section: int = 0,
                                          sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """向第一主角添加该角色的对话内容"""
        self._add_dialog_sentence_to_role(self.first_role,
                                          sents=sents,
                                          section=section,
                                          sents_dict=sents_dict)

    def add_include_sentence_to_first_role(self,
                                           sents: Optional[Union[str, List[str]]] = None,
                                           section: int = 0,
                                           sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """向第一主角添加包含该角色名字的语句"""
        self._add_include_sentence_to_role(self.first_role,
                                           sents=sents,
                                           section=section,
                                           sents_dict=sents_dict)

    def add_dialog_sentence_to_second_role(self,
                                           sents: Optional[Union[str, List[str]]] = None,
                                           section: int = 0,
                                           sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """向第二主角中添加该角色的对话内容"""
        self._add_dialog_sentence_to_role(self.second_role,
                                          sents=sents,
                                          section=section,
                                          sents_dict=sents_dict)

    def add_include_sentence_to_second_role(self,
                                            sents: Optional[Union[str, List[str]]] = None,
                                            section: int = 0,
                                            sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """向第二主角添加包含该角色名字的语句"""
        self._add_include_sentence_to_role(self.second_role,
                                           sents=sents,
                                           section=section,
                                           sents_dict=sents_dict)

    def add_dialog_sentence_to_role(self,
                                    role_name: str,
                                    sents: Optional[Union[str, List[str]]] = None,
                                    section: int = 0,
                                    sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """根据角色名字，向该角色中添加对话内容"""
        # 首先根据名字获取该角色的对象
        role = self.get_role_according_name(role_name)
        self._add_dialog_sentence_to_role(role,
                                          sents=sents,
                                          section=section,
                                          sents_dict=sents_dict)

    def add_include_sentence_to_role(self,
                                     role_name: str,
                                     sents: Optional[Union[str, List[str]]] = None,
                                     section: int = 0,
                                     sents_dict: Optional[Dict[int, Union[str, List[str]]]] = None):
        """根据角色名字，向该角色中添加包含该角色名字的语句"""
        # 首先根据名字获取该角色的对象
        role = self.get_role_according_name(role_name)
        self._add_include_sentence_to_role(role,
                                           sents=sents,
                                           section=section,
                                           sents_dict=sents_dict)


