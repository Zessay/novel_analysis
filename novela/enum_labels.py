# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-22
from typing import Dict
import os
import json
from novela._utils.metaclass import LabelEnumMeta, LoadEnumInterface


ENUM_NAMES = []


class LabelEnum(LoadEnumInterface, metaclass=LabelEnumMeta):
    r"""
    Base of all label enum
    """


def lazy_load_enums(path: str):
    """根据路径中的文件将类别加载成枚举类"""
    files = os.listdir(path)
    for file in files:
        # 首先根据文件名获取类的中文名
        enum_cn_name, enum_name = file.split("_")
        enum_name = enum_name[:-5]
        global ENUM_NAMES
        if enum_name not in ENUM_NAMES:
            with open(os.path.join(path, file), 'r', encoding="utf-8") as f:
                data = json.load(f)
            result_dict = arrange_as_dict(data)
            # 定义该枚举类并添加到全局变量中
            globals()[enum_name] = LabelEnum(enum_name, result_dict)
            # 为每个枚举类定义中文名的常规属性（这个属性不属于枚举属性）
            # 这个操作必须在枚举类定义结束之后执行
            globals()[enum_name].cn_name = enum_cn_name
            ENUM_NAMES.append(enum_name)


def arrange_as_dict(data: Dict):
    """根据原始数据中的字段组织成枚举类数据域的键值对"""
    result_dict = {}
    for i, (cls_name, cls_dict) in enumerate(data.items()):
        # 如果当前字典中包含children这个字段
        # 则首先生成children这个枚举类
        # child枚举类的名称就是对应的var_name的title形式
        if "children" in cls_dict:
            var_name = cls_dict["var_name"]
            children = cls_dict["children"]
            description = None if "description" not in cls_dict else cls_dict["description"]
            # 先获取第二层级特征的枚举类类名
            children_enum_name = var_name.title()
            # 在全局变量中定义该children的枚举类
            if len(children) <= 0:
                item_list = [i, cls_name, description, None]
            else:
                gen_children_enum_class(enum_name=children_enum_name,
                                        enum_cn_name=cls_name,
                                        data=cls_dict["children"])
                item_list = [i, cls_name, description, globals()[children_enum_name]]
            result_dict[var_name] = item_list
        elif "var_name" in cls_dict and "description" in cls_dict:
            item_list = [i, cls_name, cls_dict["description"]]
            result_dict[cls_dict["var_name"]] = item_list
        elif "var_name" in cls_dict:
            item_list = [i, cls_name]
            result_dict[cls_dict["var_name"]] = item_list
        else:
            raise ValueError('At least, `var_name` should be in the "enum_dict".')

    return result_dict


def gen_children_enum_class(enum_name: str, enum_cn_name: str, data: Dict):
    """用于生成enum中children的枚举类"""
    global ENUM_NAMES
    if enum_name not in ENUM_NAMES:
        result_dict = arrange_as_dict(data)
        globals()[enum_name] = LabelEnum(enum_name, result_dict)
        globals()[enum_name].cn_name = enum_cn_name    # 定义孩子枚举类的中文类别名
        # 将定义好的枚举类类名保存，便于动态加载
        ENUM_NAMES.append(enum_name)



if __name__ == '__main__':
    Source = LabelEnum("Source", {"YC": [1, "原创"], "TV": [2, "漫改"]})

    print(LabelEnum.__subclasses__())
    print(Source.YC.value)
    print(Source.YC.display_name)