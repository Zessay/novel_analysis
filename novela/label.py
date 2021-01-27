# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-26
from typing import List
from dataclasses import dataclass


@dataclass
class BaseInfo(object):
    source: str = None                     # 对应“是否原创”
    serial: str = None                     # 对应“连载状况”
    original_author: str = None            # 对应“原著作者”
    comic_script_writer: str = None        # 对应“漫画编剧”
    comic_editor: str = None               # 对应“漫画主笔”
    user_gender: str = None                # 对应“男频|女频”
    gender_compatible: str = None          # 对应“是否兼容男女频”


@dataclass
class ImageInfo(object):
    comic_effect: str = None               # 对应“画面效果”
    comic_force: str = None                # 对应“画面表现力”
    comic_type: str = None                 # 对应“漫画类型”


@dataclass
class StoryInfo(object):
    major_storyplot_first: str = None             # 对应“主要情节第一层”
    major_storyplot_second: str = None            # 对应“主要情节第二层”
    minor_storyplot_first: str = None             # 对应“次要情节第一层”
    minor_storyplot_second: str = None            # 对应“次要情节第二层”
    story_time: str = None                        # 对应“故事时间”
    story_culture: str = None                     # 对应“故事文化背景”
    special_space_time: str = None                # 对应“特殊时空”
    story_space: str = None                       # 对应“故事空间”
    content_style: str = None                     # 对应“内容风格”
    special_setting: List[str] = None             # 对应“特殊设定-关键词1、2”（两个词）
    story_routine: List[str] = None               # 对应“故事套路-关键词1、2”（两个词）


@dataclass
class RoleInfo(object):
    role_type: str = None                        # 对应“角色物种”
    role_target: str = None                      # 对应“角色初始目标”
    role_job: str = None                         # 对应“角色职业”
    role_personality: List[str] = None           # 对应“角色性格”（两个关键词）
    role_appearance: str = None                  # 对应“角色外形特点”
    role_identity: str = None                    # 对应“角色身份卖点”
    role_figure: str = None                      # 对应“角色形象卖点”
    role_behavior: str = None                    # 对应“角色行为卖点”
    role_contrast: str = None                    # 对应“角色反差卖点”


@dataclass
class OtherInfo(object):
    hot_topic: str = None                        # 对应“话题热点”
    other_points: List[str] = None               # 对应“其他卖点”（多个用/分开）


class Label(object):
    def __init__(self):
        self.base_info = BaseInfo()                          # 基本信息
        self.story_info = StoryInfo()                        # 故事信息
        self.first_role = RoleInfo()                         # 第一主角信息
        self.second_role = RoleInfo()                        # 第二主角信息
        self.others = OtherInfo()                            # 其他信息
        # 还有角色之间的一些标签
        self.major_roles_relation_first: str = None          # 对应“核心人物关系（第一层）”
        self.major_roles_relation_second: str = None         # 对应“核心人物关系（第二层）”
        self.major_roles_relation_routine: List[str] = None  # 对应“主要人物关系套路”（两个关键词）
        self.special_ability: str = None                     # 对应“特殊能力”
        self.plugin: str = None                              # 对应“外挂”
