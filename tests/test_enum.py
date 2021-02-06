# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-26
from novela import LabelEnum, ENUM_NAMES


# for enum_name in ENUM_NAMES:
#     print(LabelEnum.load_class(enum_name).cn_name)


print(LabelEnum.__subclasses__())
print(hasattr(LabelEnum.load_class("Source").YC, "description"))
print(getattr(LabelEnum.load_class("Source").YC, "display_name"))