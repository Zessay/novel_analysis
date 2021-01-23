# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-22
import os
from novela._utils.metaclass import LabelEnumMeta, LoadEnumInterface


class LabelEnum(LoadEnumInterface, metaclass=LabelEnumMeta):
    r"""
    Base of all label enum
    """

# # 加载文件
# with open(constants.LABELS, "r", encoding="utf-8") as f:
#     configs = json.load(f)
#
#
#
# config = configs[0]




# def lazy_load_enums(path: str):
#     files = os.listdir(path)
#     for file in files:


if __name__ == '__main__':
    Source = LabelEnum("Source", {"YC": 1, "TV": 2})

    print(LabelEnum.__subclasses__())
    print(Source.YC.value)