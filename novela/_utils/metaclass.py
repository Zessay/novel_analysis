# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-22
import inspect
import enum
from typing import Iterable, Any


class LabelEnumMeta(enum.EnumMeta):
    """用于单层枚举类的元类"""
    def __new__(mcs, name, bases, attrs):
        obj = super().__new__(mcs, name, bases, attrs)
        obj._value2member_map_ = {}
        # value表示这个值对应的索引
        # display_name表示这个枚举类对应的中文名
        # description对应该枚举类的描述
        # children对应存在二级类别的枚举类
        for m in obj:
            if isinstance(m.value, (tuple, list)):
                if len(m.value) == 2:
                    value, display_name = m.value
                    m._value_ = value
                    m.display_name = display_name
                    m.children = None
                elif len(m.value) == 3:
                    value, display_name, description = m.value
                    m._value_ = value
                    m.display_name = display_name
                    m.description = description
                    m.children = None
                elif len(m.value) == 4:
                    value, display_name, description, children = m.value
                    m._value_ = value
                    m.display_name = display_name
                    m.description = description
                    m.children = children
                else:
                    value = m.value
            else:
                value = m.value
            obj._value2member_map_[value] = m
        return obj


class LoadEnumInterface(enum.Enum):
    """用于动态加载枚举类"""
    @classmethod
    def get_all_subclasses(cls) -> Iterable[Any]:
        """
        Return a generator of all subclasses
        """
        for subclass in cls.__subclasses__():
            yield from subclass.get_all_subclasses()
            yield subclass

    @classmethod
    def load_class(cls, class_name) -> Any:
        """
        Return a subclass of ``class_name``, case insensitively
        :param cls_name (str): target class name
        :return:
        """
        result = None
        for subclass in cls.get_all_subclasses():
            # print(subclass.__name__.lower())
            if subclass.__name__.lower() == class_name.lower():
                if result is None:
                    result = subclass
                else:
                    raise RuntimeError('There are two classes with the name "{}" located at "{}" and "{}". '
                                       'You have to remove one of them to make "load_class" work normally.'.format(
                        class_name, inspect.getfile(result), inspect.getfile(subclass)))
        return result