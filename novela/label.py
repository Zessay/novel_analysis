# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-26
from typing import List, Union
from collections import OrderedDict

from novela import LabelEnum, logger


class BaseLabel:
    def __init__(self,
                 enum_name: str = None,
                 name: str = None):
        """
        这是所有标签的类
        :param enum_name: str型，表示该标签对应的枚举类的类名（英文类名）
        :param name: str型，对于一些特殊的类，可以自行指定名称（不能同时为空）
        """
        if enum_name is not None:
            try:
                self._enum_class = LabelEnum.load_class(enum_name)
                if name is not None:
                    self.name = name
                else:
                    self.name = self._enum_class.cn_name
            except:
                logger.error(f"`{enum_name}`这个枚举类没有定义!")
                raise RuntimeError(f"`{enum_name}` is undefined!")
        else:
            self._enum_class = None
            self.name = name

        self._value = None   # 表示标签值

        self.enum_names = []
        self.enum_values = []
        self.display_names = []
        self.descriptions = []
        if self._enum_class is not None:
            self._init_enum_attrs()

    def _init_enum_attrs(self):
        for item in self._enum_class:
            self.enum_names.append(item.name)   # enum_names对应的是枚举类类别的英文名
            self.enum_values.append(item.value)
            if hasattr(item, "display_name"):
                self.display_names.append(item.display_name)
            if hasattr(item, "description"):
                self.descriptions.append(item.description)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Union[str, List[str]]):
        if (v is not None) and (len(self.display_names) > 0):
            if isinstance(v, str):
                v_list = [v]
            else:
                v_list = v
            for v_item in v_list:
                if v_item not in self.display_names:
                    raise ValueError(f"`{v}`不存在于当前枚举类的标签中`{self.display_names}`!!")
            self._value = v


    @property
    def enum_class(self):
        return self._enum_class

    @enum_class.setter
    def enum_class(self, ec: Union[LabelEnum, str]):
        if isinstance(ec, LabelEnum):
            self._enum_class = ec
        else:
            self._enum_class = LabelEnum.load_class(ec.title())
        # 定义完当前的枚举类之后，需要获取其中的一些参数
        if self._enum_class is not None:
            self._init_enum_attrs()

    def __iter__(self):
        yield from self.enum_class

    def get_enum_according_display_name(self, display_name: str):
        for item in self.enum_class:
            if hasattr(item, "display_name"):
                if item.display_name == display_name:
                    return item

    def get_enum_according_value(self, value: int):
        for item in self.enum_class:
            if item.value == value:
                return item

    def to_json(self):
        if self._value is not None and isinstance(self._value, list):
            value = "，".join(self._value)
        else:
            value = self._value
        return {self.name: value}


class StringLabel:
    def __init__(self,
                 name: str=None,
                 value: str=None):
        self.name = name
        self.value = value

    def to_json(self):
        return {self.name: self.value}


# --------------------------------------------------------


class InfoInterface:
    """所有标签信息类的父类"""
    def to_json(self):
        result = OrderedDict()
        custom_attrs = [attr for attr in dir(self)
                        if ((not callable(getattr(self, attr))) and (not attr.startswith("__")))]
        for attr in custom_attrs:
            attr_value = getattr(self, attr)
            if isinstance(attr_value, StringLabel) or isinstance(attr_value, BaseLabel):
                result.update(attr_value.to_json())
        return result


class BaseInfo(InfoInterface):
    """基本信息"""
    def __init__(self):
        self.source: BaseLabel = BaseLabel(enum_name="Source")                               # 对应“是否原创”
        self.serial: BaseLabel = BaseLabel(enum_name="Serial")                               # 对应“连载状况”
        self.original_author: StringLabel = StringLabel(name="原著作者")                       # 对应“原著作者”
        self.comic_script_writer: StringLabel = StringLabel(name="漫画编剧")                   # 对应“漫画编剧”
        self.comic_editor: BaseLabel = BaseLabel(enum_name="ComicEditor")                    # 对应“漫画主笔”
        self.user_gender: BaseLabel = BaseLabel(enum_name="UserGender")                      # 对应“男频|女频”
        self.gender_compatible: BaseLabel = BaseLabel(enum_name="GenderCompatible")          # 对应“是否兼容男女频”


class ImageInfo(InfoInterface):
    """画面信息"""
    def __init__(self):
        self.comic_effect: BaseLabel = BaseLabel(enum_name="ComicEffect")               # 对应“画面效果”
        self.comic_force: BaseLabel = BaseLabel(enum_name="ComicForce")                 # 对应“画面表现力”
        self.comic_type: BaseLabel = BaseLabel(enum_name="ComicType")                   # 对应“漫画类型”


class StoryInfo(InfoInterface):
    """故事信息"""
    def __init__(self):
        self.major_storyplot_first: BaseLabel = BaseLabel(enum_name="StoryPlot",
                                                          name="主要情节（第一层）")              # 对应“主要情节第一层”
        self.major_storyplot_second: BaseLabel = BaseLabel(enum_name=None,
                                                           name="主要情节（第二层）")             # 对应“主要情节第二层”
        self.minor_storyplot_first: BaseLabel = BaseLabel(enum_name="StoryPlot",
                                                          name="次要情节（第一层）")              # 对应“次要情节第一层”
        self.minor_storyplot_second: BaseLabel = BaseLabel(enum_name=None,
                                                           name="次要情节（第二层）")             # 对应“次要情节第二层”
        self.story_time: BaseLabel = BaseLabel(enum_name="StoryTime")                          # 对应“故事时间”
        self.story_culture: BaseLabel = BaseLabel(enum_name="StoryCulture")                    # 对应“故事文化背景”
        self.special_space_time: BaseLabel = BaseLabel(enum_name="SpecialSpaceTime")           # 对应“特殊时空”
        self.story_space: BaseLabel = BaseLabel(enum_name="StorySpace")                        # 对应“故事空间”
        self.content_style: BaseLabel = BaseLabel(enum_name="StoryTime")                       # 对应“内容风格”
        self.special_setting: BaseLabel = BaseLabel(enum_name="SpecialSetting")                # 对应“特殊设定-关键词1、2”（两个词）
        self.story_routine: BaseLabel = BaseLabel(enum_name="StoryRoutine")                    # 对应“故事套路-关键词1、2”（两个词）


class RoleInfo(InfoInterface):
    """角色信息"""
    def __init__(self):
        self.role_type: BaseLabel = BaseLabel(enum_name="RoleType")                          # 对应“角色物种”
        self.role_target: BaseLabel = BaseLabel(enum_name="RoleTarget")                      # 对应“角色初始目标”
        self.role_job: BaseLabel = BaseLabel(enum_name="RoleJob")                            # 对应“角色职业”
        self.role_personality: BaseLabel = BaseLabel(enum_name="RolePersonality")            # 对应“角色性格”（两个关键词）
        self.role_appearance: BaseLabel = BaseLabel(enum_name="RoleAppearance")              # 对应“角色外形特点”
        self.role_identity: BaseLabel = BaseLabel(enum_name="RoleIdentity")                  # 对应“角色身份卖点”
        self.role_figure: BaseLabel = BaseLabel(enum_name="RoleFigure")                      # 对应“角色形象卖点”
        self.role_behavior: BaseLabel = BaseLabel(enum_name="RoleBehavior")                  # 对应“角色行为卖点”
        self.role_contrast: BaseLabel = BaseLabel(enum_name="RoleContrast")                  # 对应“角色反差卖点”


class OtherInfo(InfoInterface):
    """其他信息"""
    def __init__(self):
        self.hot_topic: BaseLabel = BaseLabel(enum_name="HotTopic")                     # 对应“话题热点”
        self.other_points: BaseLabel = BaseLabel(enum_name="OtherPoints")               # 对应“其他卖点”（多个用/分开）


# -----------------------------------------------------------


class Label:
    def __init__(self):
        self.base_info = BaseInfo()                          # 基本信息
        self.image_info = ImageInfo()
        self.story_info = StoryInfo()                        # 故事信息
        self.first_role = RoleInfo()                         # 第一主角信息
        self.second_role = RoleInfo()                        # 第二主角信息
        self.others = OtherInfo()                            # 其他信息
        # 还有角色之间的一些标签
        # 下面这些标签仍然归类到role_info这一个大类中
        self.major_roles_relation_first: BaseLabel = BaseLabel(enum_name="RoleRelation",
                                                               name="核心人物关系（第一层）")          # 对应“核心人物关系（第一层）”
        self.major_roles_relation_second: BaseLabel = BaseLabel(enum_name=None,
                                                                name="核心人物关系（第二层）")         # 对应“核心人物关系（第二层）”
        self.major_roles_relation_routine: BaseLabel = BaseLabel(enum_name="RoleRelationRoutine",
                                                                 name="主要人物关系套路")             # 对应“主要人物关系套路”（两个关键词）
        self.special_ability: BaseLabel = BaseLabel(enum_name="SpecialAbility")                    # 对应“特殊能力”
        self.plugin: BaseLabel = BaseLabel(enum_name="Plugin")                                     # 对应“外挂”

    def to_json(self):
        result = OrderedDict()
        result["基本信息"] = self.base_info.to_json()
        result["画面信息"] = self.image_info.to_json()
        result["故事信息"] = self.story_info.to_json()
        # 角色信息
        roleinfo_dict = OrderedDict()
        for key, value in self.first_role.to_json().items():
            roleinfo_dict[f"主角1-{key}"] = value
        for key, value in self.second_role.to_json().items():
            roleinfo_dict[f"主角2-{key}"] = value
        roleinfo_dict.update(self.major_roles_relation_first.to_json())
        roleinfo_dict.update(self.major_roles_relation_second.to_json())
        roleinfo_dict.update(self.major_roles_relation_routine.to_json())
        roleinfo_dict.update(self.special_ability.to_json())
        roleinfo_dict.update(self.plugin.to_json())
        # 更新角色信息
        result["角色信息"] = roleinfo_dict
        result["其他信息"] = self.others.to_json()

        return result


if __name__ == '__main__':
    baselabel = BaseLabel(name="第二层")
    baselabel.enum_class = "Test"
    print(baselabel.enum_class)
    print(baselabel.enum_names)