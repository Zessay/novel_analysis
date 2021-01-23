# coding=utf-8
# @Author: 莫冉
# @Date: 2021-01-20


class StoryLine(object):
    def __init__(self,
                 opening: str = None,
                 first_step: str = None,
                 second_step: str = None,
                 third_step: str = None,
                 fourth_step: str = None):
        """
        表示整个小说故事线
        :param opening: str型，表示小说的开篇
        :param first_step: str型，对应“起承转合”中的“起”
        :param second_step: str型，对应“起承转合”中的“承”
        :param third_step: str型，对应“起承转合”中的“转”
        :param fourth_step: str型，对应“起承转合”中的“合”
        """
        self.opening = opening
        self.first_step = first_step
        self.second_step = second_step
        self.third_step = third_step
        self.fourth_step = fourth_step
