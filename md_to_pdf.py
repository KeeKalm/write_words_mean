import os
import pypandoc


def md_to_pdf(md, pdf, css):
    pypandoc.convert_file(
        source_file=md,
        to="html",
        format="md",
        outputfile=pdf,
        extra_args=f"--css {css} --pdf-engine wkhtmltopdf".split(" ")
    )


def md_list_to_pdf(md_list, out_dir, css):
    if os.path.isfile(out_dir):
        raise FileExistsError(f"{out_dir} is file, no dir!!!")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for md in md_list:
        title = os.path.split(md)[-1].split(".md")[0]
        pdf = os.path.join(out_dir, f"{title}.pdf")

        print(f"conver {title}")

        md_to_pdf(md=md,
                  pdf=pdf,
                  css=css)


def get_md_list(dir, prefix="", infix="", suffix=""):
    md_list = list()
    if isinstance(dir, str):
        dir = dir.split(",")

    for d in dir:
        md_list += [os.path.join(d, f) for f in os.listdir(d)
                    if (os.path.isfile(os.path.join(d, f))) and (f.startswith(prefix)) and (infix in f) and (
                        f.endswith(suffix + ".md"))]

    return md_list


def __one_md(args):
    md_to_pdf(args.md, args.pdf, args.css)


def __many_md(args):
    md_list_to_pdf(md_list=get_md_list(dir=args.dir,
                                       prefix=args.prefix,
                                       infix=args.infix,
                                       suffix=args.suffix),
                   out_dir=args.out,
                   css=args.css)


def __argparse():
    """
    命令行解析
    :return:
    """
    import argparse

    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument("--css",
                        type=str,
                        default="",
                        help="css file")

    subparser = parser.add_subparsers(dest='one or many',
                                      help="one md file or many md file in dirs")

    oneparser = subparser.add_parser("one",
                                     help="one md file")
    oneparser.add_argument("md",
                           type=str)
    oneparser.add_argument("pdf",
                           type=str)
    oneparser.set_defaults(func=__one_md)

    manyparser = subparser.add_parser("many",
                                      help="one md file")
    manyparser.add_argument("dir",
                            type=str)
    manyparser.add_argument("out",
                            type=str)
    manyparser.add_argument("--prefix",
                            type=str,
                            default="")
    manyparser.add_argument("--infix",
                            type=str,
                            default="")
    manyparser.add_argument("--suffix",
                            type=str,
                            default="")
    manyparser.set_defaults(func=__many_md)

    return parser.parse_args()


if __name__ == "__main__":
    args = __argparse()
    print(args)
    args.func(args)
