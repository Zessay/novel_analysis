# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-06
import os


# --------------- 一些表征人性别的属性词 -------------------

SHE = "她"
HE = "他"
IT = "它"
TA = "ta"

# --------------- 一些文件路径 -------------------
LABELS_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/labels")
BASE_INFO = os.path.join(LABELS_BASE_PATH, "baseinfos")
IMAGE_INFO = os.path.join(LABELS_BASE_PATH, "imageinfos")
STORY_INFO = os.path.join(LABELS_BASE_PATH, "storyinfos")
ROLE_INFO = os.path.join(LABELS_BASE_PATH, "roleinfos")
OTHER_INFO = os.path.join(LABELS_BASE_PATH, "others")

# --------------- 日志文件的配置 -------------------

PACKAGE_NAME = os.path.basename(os.path.dirname(__file__))
LOG_FILE = "../novel.log"


# --------------- 预定义时用到的变量 -------------------
# 所有标签文件放在一个列表中
ALL_LABELS_PATH = [BASE_INFO, IMAGE_INFO, STORY_INFO,
                   ROLE_INFO, OTHER_INFO]