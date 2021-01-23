# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-22
import json

file = "../data/config/labels.json"

with open(file, "r", encoding="utf-8") as f:
    records = json.load(f)


print(len(records))
print(records[0])