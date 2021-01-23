# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-20
import itertools
from enum import Enum

# ----------- 定义是否原创枚举类 --------------

# 以1作为起始值而不以0，是因为0在Python中认为是False，而所有的枚举值都应该是True
_SOURCE = {
    1: ["原创", "YC"],
    2: ["小说漫改", "NOVEL"],
    3: ["影视改编", "TV"],
    4: ["游戏改编", "GAME"],
    5: ["同人", "FAN"]
}

Source = Enum(
    value="Source",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _SOURCE.items()
    )
)

# ----------- 连载状况枚举类 --------------

_SERIAL = {
    1: ["连载", "LZ"],
    2: ["完结", "WJ"]
}

Serial = Enum(
    value="Serial",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _SERIAL.items()
    )
)

# ----------- 漫画主笔枚举类 --------------

_COMIC_EDITOR = {
    1: ["主笔", "ZB"],
    2: ["工作室", "GZS"]
}

ComicEditor = Enum(
    value="ComicEditor",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COMIC_EDITOR.items()
    )
)

# ----------- 男女频枚举类 --------------

_USER_GENDER = {
    1: ["男频", "MALE"],
    2: ["女频", "FEMALE"]
}

UserGender = Enum(
    value="UserGender",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _USER_GENDER.items()
    )
)

# ----------- 是否兼容男女频枚举类 --------------

_GENDER_COMPATIBLE = {
    1: ["是", "YES"],
    2: ["否", "NO"]
}

GenderCompatible = Enum(
    value="GenderCompatible",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _GENDER_COMPATIBLE.items()
    )
)

# ----------- 画面枚举类 --------------
# 清新  时尚  暗黑  恐怖  乡土  华丽  热血效果  普通  其他
_COMIC_EFFECT = {
    1: ["清新", "QX"],
    2: ["时尚", "SS"],
    3: ["暗黑", "AH"],
    4: ["恐怖", "KB"],
    5: ["乡土", "XT"],
    6: ["华丽", "HL"],
    7: ["热血效果", "RX"],
    8: ["普通", "PT"],
    9: ["其他", "OTHER"]
}

ComicEffect = Enum(
    value="ComicEffect",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COMIC_EFFECT.items()
    )
)

# ----------- 画面表现力枚举类 --------------
# 极致  优秀  合格  粗糙
_COMIC_FORCE = {
    1: ["极致", "JZ"],
    2: ["优秀", "YX"],
    3: ["合格", "HG"],
    4: ["粗糙", "CC"]
}

ComicForce = Enum(
    value="ComicForce",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COMIC_FORCE.items()
    )
)

# ----------- 漫画类型枚举类 --------------
# 国漫风  港漫风  美漫风  日漫风  韩漫风
_COMIC_TYPE = {
    1: ["国漫风", "CH"],
    2: ["港漫风", "HK"],
    3: ["美漫风", "USA"],
    4: ["日漫风", "JP"],
    5: ["韩漫风", "KR"]
}

ComicType = Enum(
    value="ComicType",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COMIC_TYPE.items()
    )
)

# ----------- 情节第二层枚举类 --------------
# 爱情类：恋爱  纯爱  后宫  逆后宫  同性爱
_LOVE = {
    1: ["恋爱", "LA"],
    2: ["纯爱", "CA"],
    3: ["后宫", "HG"],
    4: ["逆后宫", "NHG"],
    5: ["同性爱", "TXA"]
}
# 动作类：修真  战斗  战争
_ACTION = {
    1: ["修真", "XZ"],
    2: ["战斗", "ZD"],
    3: ["战争", "ZZ"]
}
# 动作——冒险类：冒险  闯关  盗墓
_ADVENTURE = {
    1: ["冒险", "MX"],
    2: ["闯关", "CG"],
    3: ["盗墓", "DM"]
}
# 竞技类：体育 游戏 才艺 棋牌 玩具
_COMPETITION = {
    1: ["体育", "TY"],
    2: ["游戏", "YX"],
    3: ["才艺", "CY"],
    4: ["棋牌", "QP"],
    5: ["玩具", "WJ"]
}
# 脱困类：生存 越狱
_UNBOUND = {
    1: ["生存", "SC"],
    2: ["越狱", "YY"]
}
# 职场生活类：医疗 演艺 办公室
_CAREER = {
    1: ["医疗", "YL"],
    2: ["演艺", "YY"],
    3: ["办公室", "BGS"]
}
# 推理类：刑侦  破案  解谜
_ANOLOGY = {
    1: ["刑侦", "XZ"],
    2: ["破案", "PA"],
    3: ["解谜", "JM"]
}
# 日常类：美食  日常
_DAILY = {
    1: ["美食", "MS"],
    2: ["日常", "RC"]
}
# 智斗类：谍战 商战 宫斗 权谋 宅斗 豪门恩怨
_SAPIENT = {
    1: ["谍战", "DZ"],
    2: ["商战", "SZ"],
    3: ["宫斗", "GD"],
    4: ["权谋", "QM"],
    5: ["宅斗", "ZD"],
    6: ["豪门恩怨", "HMEY"]
}

Love = Enum(
    value="Love",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _LOVE.items()
    )
)
Action = Enum(
    value="Action",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _ACTION.items()
    )
)
Adventure = Enum(
    value="Adventure",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _ADVENTURE.items()
    )
)
Competition = Enum(
    value="Competition",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COMPETITION.items()
    )
)
Unbound = Enum(
    value="Unbound",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _UNBOUND.items()
    )
)
Career = Enum(
    value="Career",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _CAREER.items()
    )
)
Anology = Enum(
    value="Anology",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _ANOLOGY.items()
    )
)
Daily = Enum(
    value="Daily",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _DAILY.items()
    )
)
Sapient = Enum(
    value="Sapient",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _SAPIENT.items()
    )
)

# ----------- 情节第一层枚举类 --------------
# 爱情类 动作类 动作——冒险类 竞技类 脱困类 职场、生活类 推理类 日常类 智斗类 奇轶鬼怪 种田 个人经历 无主要情节
# 后面4个没有第2层
_STORY_TYPE = {
    (1, Love): ["爱情类", "LOVE"],
    (2, Action): ["动作类", "ACTION"],
    (3, Adventure): ["动作——冒险类", "ADVENTURE"],
    (4, Competition): ["竞技类", "COMPETITION"],
    (5, Unbound): ["脱困类", "UNBOUND"],
    (6, Career): ["职场生活类", "CAREER"],
    (7, Anology): ["推理类", "ANALOGY"],
    (8, Daily): ["日常类", "DAILY"],
    (9, Sapient): ["智斗类", "SAPIENT"],
    (10, None): ["奇轶鬼怪", "GHOST"],
    (11, None): ["种田", "FARM"],
    (12, None): ["个人经历", "EXPERIENCE"],
    (13, None): ["无主要情节", "NONE"]
}

StoryType = Enum(
    value="StoryType",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _STORY_TYPE.items()
    )
)

# ----------- 故事时间枚举类 --------------
# 年代 未来 民国 当代 远古 虚拟时代 古代 近代
_STORY_TIME = {
    1: ["年代", "ND"],
    2: ["未来", "WL"],
    3: ["民国", "MG"],
    4: ["当代", "DD"],
    5: ["远古", "YG"],
    6: ["虚拟时代", "XN"],
    7: ["古代", "GD"],
    8: ["近代", "JD"]
}

StoryTime = Enum(
    value="StoryTime",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _STORY_TIME.items()
    )
)

# ----------- 故事文化背景枚举类 --------------
# 中国 印度 埃及/巴比伦 希腊 西方欧洲 日本 韩国 虚拟文化背景 其他文化背景
_STORY_CULTURE = {
    1: ["中国", "CH"],
    2: ["印度", "IN"],
    3: ["埃及/巴比伦", "EG"],
    4: ["希腊", "GR"],
    5: ["西方欧洲", "WEU"],
    6: ["日本", "JP"],
    7: ["韩国", "KR"],
    8: ["虚拟文化背景", "XN"],
    9: ["其他文化背景", "OTHER"]
}

StoryCulture = Enum(
    value="StoryCulture",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _STORY_CULTURE.items()
    )
)

# ----------- 特殊时空枚举类 --------------
# 架空 游戏世界 女尊世界 科幻世界 九州世界观 朋克 乌托邦/反乌托邦 克苏鲁神话 东方修仙世界 ABO 山海经世界观（洪荒流） 后启示录/废土 平行世界 无
_SPECIAL_SPACETIME = {
    1: ["架空", "JK"],
    2: ["游戏世界", "YX"],
    3: ["女尊世界", "NZ"],
    4: ["科幻世界", "KH"],
    5: ["九州世界观", "JZ"],
    6: ["朋克", "PK"],
    7: ["乌托邦/反乌托邦", "WTB"],
    8: ["克苏鲁深化", "KSL"],
    9: ["东方修仙世界", "DXX"],
    10: ["ABO"],
    11: ["山海经世界观（洪荒流）", "SHJ"],
    12: ["后启示录/废土", "FT"],
    13: ["平行世界", "PXSJ"],
    14: ["无", "NONE"]
}

SpecialSpacetime = Enum(
    value="SpecialSpacetime",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _SPECIAL_SPACETIME.items()
    )
)

# ----------- 故事空间枚举类 --------------
# 都市 乡村 宫廷 校园 职场 军旅 市井 医院 异世界 城池 星际 郊野 未固定空间 居住空间 娱乐圈空间 其他
_STORY_SPACE = {
    1: ["都市", "DS"],
    2: ["乡村", "XC"],
    3: ["宫廷", "GT"],
    4: ["校园", "XY"],
    5: ["职场", "ZC"],
    6: ["军旅", "JL"],
    7: ["市井", "SJ"],
    8: ["医院", "YY"],
    9: ["异世界", "YSJ"],
    10: ["城池", "CC"],
    11: ["星际", "XJ"],
    12: ["郊野", "JY"],
    13: ["未固定空间", "WGD"],
    14: ["居住空间", "JZ"],
    15: ["娱乐圈空间", "YLQ"],
    16: ["其他", "OTHER"]
}
StorySpace = Enum(
    value="StorySpace",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _STORY_SPACE.items()
    )
)

# ----------- 内容风格枚举类 --------------
# 励志 热血 爆笑 幽默 治愈 惊悚 恐惧 悬疑 轻松 甜宠 虐心 愤怒 小确幸 压抑
_CONTENT_STYLE = {
    1: ["励志", "LZ"],
    2: ["热血", "RX"],
    3: ["爆笑", "BX"],
    4: ["幽默", "YM"],
    5: ["治愈", "ZY"],
    6: ["惊悚", "JS"],
    7: ["恐惧", "KJ"],
    8: ["悬疑", "XY"],
    9: ["轻松", "QS"],
    10: ["甜宠", "TC"],
    11: ["虐心", "NX"],
    12: ["愤怒", "FN"],
    13: ["小确幸", "XQX"],
    14: ["压抑", "YY"]
}
ContentStyle = Enum(
    value="ContentStyle",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _CONTENT_STYLE.items()
    )
)
# ----------- 特殊设定枚举类 --------------
# 穿越 身穿 魂穿 反穿 快穿 重生 变异 末世 生化危机 多世情缘 系统 转世 失忆 男扮女装 女扮男装 性转 随身空间 带球跑
# 炉鼎 突发任务 灵魂出窍（人鬼情未了） 游戏 大逃杀模式 寄生 突获“力量” 休眠觉醒 封印 炮灰婚嫁


# ----------- 故事套路枚举类 --------------
# 复仇虐渣 咸鱼翻身（废柴逆袭） 追妻火葬场 无敌流


# ----------- 角色物种枚举类 --------------
# 人类 兽人 半兽人 兽族 吸血鬼 狼人 外星人 机器人 精神体 僵尸 龙族 神族 狐狸精 动物 怪物 魔族 妖族 精灵 丧尸 系统NPC


# ----------- 角色初始目标枚举类 --------------
# 复仇 变强 赚钱 完成使命/义务 洗刷耻辱/冤屈揭秘  揭秘 生活上的愉悦  追求某人 满足野心  生存  保护/救出亲友  保住个人地位/名誉 守护恋情 寻找自我价值

# ----------- 角色职业枚举类 --------------
# 丞相|摄政王|首辅|将军|仵作|捕快|知府|御史|大理寺卿|师爷|士兵|侍卫|画师|太医|弟子|护法|杀手|绣娘|郎中|农民|村长|妓女|艺妓|男妓|舞姬|书生|
# 丫鬟|镖师|土匪|风水师|道士|捞尸人|蛊师|卦师|占卜师|和尚|喇嘛|尼姑|艺人|导演|歌手|演员|模特|制片人|编剧|经纪人|少帅|少将|特工|军医|警察|
# 法医|球员|电竞选手|赛车手|佣兵|间谍|卧底|侦探|黑客|入殓师|宇航员|盗墓者|欺诈师|老师|教练|网络主播|总裁|律师|医生|记者|司机|厨师|保镖|护士|
# 白领|学生|设计师|家教|心理咨询师|声优|牛郎|编辑|助理|魔术师|老板|漫画家|店长|精神科医生|快递员|科研人员|教授|程序员|飞行员|造型师|服务员|
# 调香师|猎人|饲养员|风水师|总统|鬼差|月老|瘟神|死神|冥王|牧师 |魔法师|召唤师|驱魔师|骑士|剑士|冒险家|梦境师|无业|修真者|画手|写手|赏金猎人|
# 游戏DPS|游戏MT|游戏辅助|管家/执事|职业英雄|消防员|锻造师/工匠|船长|船员/水手

# ----------- 角色性格枚举类 --------------
# 表里不一 傲娇 腹黑 高冷 逗逼 淡定 刁蛮 单纯 霸道 理想主义 幽默 狡猾 叛逆 幼稚 勇敢 阴暗 神经质 深沉 自负
# 果断 自恋 大大咧咧 率性 懦弱 多愁善感 玻璃心 孤僻 仗义 害羞 纯真 狂妄 古灵精怪 机智 冷酷 乐于助人 外热内冷 温柔 阴险 呆萌


# ----------- 角色外形特点枚举类 --------------
# 萝莉 正太 丑女 兽耳 翅膀 尾巴 胖子 灵体 双马尾 黑长直 动物形态 黑皮 萌宠 阴阳人

# ----------- 角色身份卖点枚举类 --------------
# 皇上 女帝 太子 皇子 皇后 皇妃 权臣 王爷 公主 废后 门主 掌门 家主 少主 首徒 武林盟主 网红 富二代 富家千金 落魄千金 宠妃 农女
# 寡妇 孤儿 剩女 备胎 替身 私生子 弃妇 兵王 校花 校草 男神 女神 土豪 鬼夫 童养媳 赘婿 偶像 女官花魁 老板娘 黑道人士 男配 女配
# 暴君 凤凰男 嫡女 庶女 庶子 纨绔 败家子 废柴 穷人 学霸

# ----------- 角色形象卖点枚举类 --------------
# 御姐 霸总 大叔 伪娘 萌宝 女王 油腻男 绿茶婊 人妻属性 黑莲花

# ----------- 角色行为卖点枚举类 --------------
# 颜控 花痴 兄控 弟控 声控 中央空调 异性恐惧症 大胃王 感情迟钝 忠犬 圣母 宅 腐 无口系 拜金女 话痨 毒舌 变身 妄想 异装癖 收藏癖 恋物癖
# 好色 戏精 扮猪吃虎 中二


# ----------- 角色反差卖点枚举类 --------------
# 多重人格 暴力萝莉 柔情铁汉 童颜巨乳


# ----------- 核心人物关系枚举类 --------------
# 第一层
# 亲人关系 爱恋关系 友情关系 职场、社会关系 敌对关系 身份替身 利用关系 饲养 囚禁

# 第二层
# 亲人关系：婆媳 兄（弟姐）妹  父（母子）女  祖孙
# 爱恋关系：恋人 夫妻 暗恋 青梅竹马 情人 年下恋人 契约恋人 先婚后爱 初恋 隐婚 未婚夫妻 暧昧 暗恋 单恋 契约婚恋 前任
# 友情关系：普通朋友 哥们 闺蜜 红颜/蓝颜知己
# 职场、社会关系：师徒 师生 主仆 君臣 同桌 雇佣 同事 同学 校友 同门 同行
# 敌对关系：劲敌 宿敌 情敌
# 身份替身：
# 利用关系：
# 饲养：
# 囚禁：

# ----------- 主要人物关系套路枚举类 --------------
# 亦敌亦友 贫穷女富贵男 贫穷男富贵女 青梅竹马 契约恋人 欢喜冤家 先婚后爱 相爱相杀 铁三角


# ----------- 特殊能力枚举类 --------------
# 读心术 预言术 炼药术 透视 阴阳眼 瞬间转移 吸食怨气 穿越时空 掌控时间 快速愈合 超级力量 变形 魔法/法术


# ----------- 外挂枚举类 --------------
# 导师 女友 男友 同伴 金钱 秘籍 天材地宝 武器 绝技 系统 随身空间

# ----------- 其他卖点枚举类 --------------
# 萌宝 宠物 福利 耽美 百合 伪耽美 伪百合



if __name__ == '__main__':
    # print(Source["YC"].name)
    # print(Source.YC.name)
    # print(Source.YC.value)
    print(StoryType.LOVE.name)
    # print(StoryType(1))
    print(SpecialSpacetime(10).name)