# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-26
import novela.constants as constants
from novela.enum_labels import lazy_load_enums, LabelEnum, ENUM_NAMES
from novela.utils.common import init_logger


if len(ENUM_NAMES) == 0:
    # 预定义所有的枚举类
    for path in constants.ALL_LABELS_PATH:
        lazy_load_enums(path)

    # 配置logger的对象
    logger = init_logger(constants.LOG_FILE)
    logger.info(f"共计定义了 {len(ENUM_NAMES)} 个枚举类，包含{', '.join(ENUM_NAMES)}")


__all__ = ["LabelEnum", "logger", "ENUM_NAMES"]
