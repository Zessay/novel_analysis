# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-03
import numpy as np
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


def autolabel(rects: List[Rectangle], ax: Axes):
    """
    对每个矩形进行标注
    :param rects: 这里面的每一个元素表示直方图中的每一个矩形
    :param ax: 这个表示直方图中的一幅图
    :return:
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")


def plot_bar(x_labels: List[str],
             y: List[float],
             y_label: str = "",
             save_filename: str = "save.png",
             font: fm.FontProperties = None,
             plt_style: str = "ggplot",
             figsize: Optional[Tuple[int]] = None,
             gap: float = 3.0):
    """
    绘制直方图
    :param x_labels: List[str]，表示直方图中每一个矩形的名称
    :param y: List[float]，表示直方图每一个举行的高度
    :param y_label: str型，表示y轴的标注
    :param save_filename: str型，表示保存图片的名称
    :param font: 如果需要修改中文默认字体，则需要指定这个参数
    :param plt_style: str型，表示绘图的风格，默认为`ggplot`
    :param figsize: Tuple[int]型，表示画布的大小
    :return:
    """
    # 正常显示中文字体，默认字体为微软雅黑
    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
    plt.style.use(plt_style)      # 如果想要使用ieee，需要使用https://github.com/garrettj403/SciencePlots
    # 获取x轴标签的数量
    x = np.arange(len(x_labels))
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1,1,1)
    rects = ax.bar(x, y, color="royalblue", alpha=0.7)

    # 添加一些标注
    if y_label:
        ax.set_ylabel(y_label, fontproperties=font)
    # 设置y轴的最小值和最大值
    y_low, y_high = min(y), max(y)
    y_low = 0 if y_low >= 0 else y_low - gap
    y_high = y_high + gap
    ax.set_ylim(y_low, y_high)
    ax.set_xticks(x)    # 设置每一个直方图矩形所在的位置
    ax.set_xticklabels(x_labels, fontproperties=font)

    # 给矩形添加标注
    autolabel(rects, ax)
    fig.savefig(save_filename, bbox_inches="tight", dpi=300)


def get_font(font_path: str, font_size: int = 10) -> fm.FontProperties:
    """
    获取字体类
    :param font_path: str型，表示字体的路径
    :param font_size: int型，表示字体的大小
    :return:
    """
    font = fm.FontProperties(fname=font_path, size=font_size)
    return font


if __name__ == '__main__':
    font_path = r"C:\Windows\Fonts\SIMLI.TTF"
    font = get_font(font_path)

    # print(type(font))
    x_labels = ["中文1", "英文2"]
    y = [10, 8]

    plot_bar(x_labels, y, font=font)