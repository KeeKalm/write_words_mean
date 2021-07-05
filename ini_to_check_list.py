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

        @property
        def data(self):
            return self._ww

        def add(self, word_items, seed=None):
            """
            添加一组单词清单
            :param word_items:
            :param seed:
            :return:
            """
            self._ww += word_items
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

    def __init__(self,
                 word_file: str,
                 use_timestamp: bool = True,
                 section_list: List[str] = ["word", "forget"],
                 encoding="utf-8"):

        self._title = os.path.split(word_file)[-1].split(".")[0]
        self._use_timestamp = use_timestamp
        self._ww = self.__WordWord([])

        if os.path.isfile(word_file):
            self.__read_file(word_file, encoding, section_list)

    def __read_file(self, word_file, encoding, section_list):
        self._f = ConfigParser(allow_no_value=True)
        self._f.read(word_file, encoding=encoding)

        if ("word" in section_list) and (self._f.has_section("word")):
            self._ww.add(self._f.items("word"))

        if ("forget" in section_list) and (self._f.has_section("forget")):
            self._ww.add(self._f.items("forget"))

    @property
    def data(self):
        return self._ww.data

    def add(self, word_list):
        self._ww.add(word_list.data)

    def to_file_rand(self, out_dir: str = "out", tag: str = ""):
        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass

        self._ww.rand_list()

        file_name = f"{self._title}_{tag}_听写_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.md" if self._use_timestamp else f"{self._titile}_{tag}_听写.md"
        self.__wordword_to_file(self._ww.make_list_random_no_note(),
                                os.path.join(out_dir, file_name))

        file_name = f"{self._title}_{tag}_答案_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.md" if self._use_timestamp else f"{self._titile}_{tag}_答案.md"
        self.__wordword_to_file(self._ww.make_list_random_note(),
                                os.path.join(out_dir, file_name))

    def __wordword_to_file(self,
                           ww: List[Tuple[str, str]],
                           file_path: str):
        ww_l = []
        for i in range(len(ww)):
            ww_l.append(f"{i}. {ww[i][0]}\t\t{ww[i][1]}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\r\n".join(ww_l))


def __argparse():
    """
    命令行解析
    :return:
    """
    import argparse

    def str2bool(s: str):
        return True if s.lower() == "true" else False

    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument("word_files", type=str,
                        help="many word list word ini files that use [word] and maybe use [forget] , ex. Unit1.ini,Unit2.ini")
    parser.add_argument("--use_forget", type=str2bool, default=False, help="Do use [forget] in word_files?")
    parser.add_argument("--out_dir", type=str, default="out", help="out dir for write word files")
    parser.add_argument("--use_timestamp", type=str2bool, default=True, help="Do use timestamp in output file?")
    parser.add_argument("--forget_files", type=str, default="",
                        help="many word list forget ini files that use [forget] , ex. Unit1.ini,Unit2.ini")

    # tag
    tag_parsers = parser.add_subparsers(dest='tag', help="Do use tag in output files?")
    ## no tag
    no_tag_parsers = tag_parsers.add_parser('no_tag', help='build specify the number of files without tag')
    no_tag_parsers.add_argument("file_number", type=int, help="the number of output files")
    no_tag_parsers.set_defaults(func=__no_tag)
    ## same tag
    same_tag_subparser = tag_parsers.add_parser('same_tag', help='build specify the number of files with same tag')
    same_tag_subparser.add_argument("file_number", type=int, help="the number of output files")
    same_tag_subparser.add_argument("tag", type=str, help="file tag")
    same_tag_subparser.set_defaults(func=__same_tag)
    ## tag list
    list_tag_subparser = tag_parsers.add_parser('list_tag',
                                                help='build specify the number of the list of tag of files with the list of tag')
    list_tag_subparser.add_argument('tag_list', type=str, help="file tag list")
    list_tag_subparser.add_argument('--use_order', type=str2bool, default=True,
                                    help="Do use the order number of tag list?")
    list_tag_subparser.set_defaults(func=__list_tag)

    return parser.parse_args("Unit7-1.ini --forget_files word.ini no_tag 1".split(" "))


def __make_word_object(args) -> WordList:

    use_timestamp = args.use_timestamp

    word_files = [i for i in args.word_files.replace(" ", "").split(",") if os.path.isfile(i)]
    word_sections = ["word", "forget"] if args.use_forget else ["word"]

    forget_files = [i for i in args.forget_files.replace(" ", "").split(",") if os.path.isfile(i)]
    forget_sections = ["forget"]

    all_number = len(word_files) + len(forget_files)

    if all_number <= 0:
        w = WordList("Null", use_timestamp, [])
    elif all_number > 1:
        if len(word_files) == 1:
            w = WordList(word_files[0], use_timestamp, word_sections)
        else:
            w = WordList(f"{all_number}files", use_timestamp, [])
            for i in word_files:
                w.add(WordList(i, use_timestamp, word_sections))
        for i in forget_files:
            w.add(WordList(i, use_timestamp, forget_sections))

    elif all_number == 1:
        if len(word_files) == 1:
            w = WordList(word_files[0], use_timestamp, word_sections)
        else:
            w = WordList(forget_files[0], use_timestamp, forget_sections)
    return w


def __no_tag(args):
    w = __make_word_object(args)
    for i in range(args.file_number):
        w.to_file_rand(out_dir=args.out_dir,
                       tag=str(i + 1))


def __same_tag(args):
    w = __make_word_object(args)
    for i in range(args.file_number):
        w.to_file_rand(out_dir=args.out_dir,
                       tag=f"{i + 1}_{args.tag}")


def __list_tag(args):
    w = __make_word_object(args)
    tag_list = args.tag_list
    if tag_list.endswith(","):
        tag_list = tag_list[:-1]
    tag_list = tag_list.split(",")
    for i in range(len(tag_list)):
        tag = f"{i + 1}_{tag_list[i]}" if args.use_order else f"{tag_list[i]}"
        w.to_file_rand(out_dir=args.out_dir,
                       tag=tag)


if __name__ == "__main__":
    args = __argparse()
    print(args)
    args.func(args)
