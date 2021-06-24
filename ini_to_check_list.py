from configparser import ConfigParser
import random
import os
import datetime
from typing import List, Tuple


class WordList:
    class __ListInfo:
        pass

    class __WordWord:
        """
        单词字段列表
        """

        def __init__(self, word_items: List[Tuple[str, str]], seed=None):
            self._ww = word_items
            self._wwr = []
            self.rand_list(seed)

        def rand_list(self, seed=None):
            """
            随机一次列表
            :param seed:
            :return:
            """
            random.seed(None)
            self._wwr = random.sample(self._ww, len(self._ww))

        def make_list_no_random_no_note(self) -> List[Tuple[str, str]]:
            """
            产生不随机，不注释的列表
            :return:
            """
            return [(i[0], "") for i in self._ww]

        def make_list_random_no_note(self) -> List[Tuple[str, str]]:
            """
            产生随机，不注释的列表
            :return:
            """
            return [(i[0], "") for i in self._wwr]

        def make_list_no_random_note(self) -> List[Tuple[str, str]]:
            """
            产生不随机，注释的列表
            :return:
            """
            return self._ww

        def make_list_random_note(self) -> List[Tuple[str, str]]:
            """
            产生随机，注释的列表
            :return:
            """
            return self._wwr

    def __init__(self, word_file: str, encoding="utf-8"):
        if not os.path.isfile(word_file):
            raise Exception(f"{word_file} not a file")

        self._titile = os.path.split(word_file)[-1].split(".")[0]

        self._f = ConfigParser(allow_no_value=True)
        self._f.read(word_file, encoding=encoding)

        if not self._f.has_section("word"):
            word_list = []
        else:
            word_list = self._f.items("word")

        self._ww = self.__WordWord(word_list)

    def to_file_rand(self, out_dir: str="out", tag: str=""):
        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass

        self._ww.rand_list()

        wwnn = self._ww.make_list_random_no_note()
        wwn = self._ww.make_list_random_note()

        self.__wordword_to_file(self._ww.make_list_random_no_note(), 
                                os.path.join(out_dir, 
                                             f"{self._titile}_{tag}_听写_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.md"))
        self.__wordword_to_file(self._ww.make_list_random_note(), 
                                os.path.join(out_dir,
                                             f"{self._titile}_{tag}_答案_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.md"))
    def __wordword_to_file(self,
                           ww: List[Tuple[str, str]],
                           file_path: str):
        ww_l = []
        for i in range(len(ww)):
            ww_l.append(f"{i}. {ww[i][0]}\t\t{ww[i][1]}")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\r\n".join(ww_l))
        

if __name__ == "__main__":
    w = WordList("Unit7-1.ini")
    for i in range(9):
        w.to_file_rand(tag = i + 1)
    pass
