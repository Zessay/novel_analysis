# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-26
from novela import LabelEnum


print(LabelEnum.__subclasses__())
print(LabelEnum.load_class("Source").YC.description)