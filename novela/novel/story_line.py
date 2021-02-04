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

    def add_info_to_storyline(self, **kwargs):
        if "opening" in kwargs:
            self.opening = kwargs.get("opening")
        if "first_step" in kwargs:
            self.first_step = kwargs.get("first_step")
        if "second_step" in kwargs:
            self.second_step = kwargs.get("second_step")
        if "third_step" in kwargs:
            self.third_step = kwargs.get("third_step")
        if "fourth_step" in kwargs:
            self.fourth_step = kwargs.get("fourth_step")
