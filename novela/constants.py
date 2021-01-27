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
# LABELS = "../data/config/labels.json"
LABELS_BASE_PATH = "../data/labels"
BASE_INFO = os.path.join(LABELS_BASE_PATH, "baseinfos")
IMAGE_INFO = os.path.join(LABELS_BASE_PATH, "imageinfos")
STORY_INFO = os.path.join(LABELS_BASE_PATH, "storyinfos")
ROLE_INFO = os.path.join(LABELS_BASE_PATH, "roleinfos")
OTHER_INFO = os.path.join(LABELS_BASE_PATH, "others")

# --------------- 日志文件的配置 -------------------

PACKAGE_NAME = os.path.basename(os.path.dirname(__file__))
LOG_FILE = "../novel.log"


# --------------- 预定义时用到的变量 -------------------
ALL_LABELS_PATH = [BASE_INFO, IMAGE_INFO, STORY_INFO,
                   ROLE_INFO, OTHER_INFO]