#!/usr/bin/env python
from __future__ import absolute_import, print_function

import argparse
import importlib.util
import os
import subprocess

import mkrst_themes

THEMES_DIR = os.path.dirname(mkrst_themes.__file__)

THEME = "default"
SUPPORTED_FORMATS = "html pdf odt".split()

DEBUG = "DEBUG" in os.environ


class CommandExecutor:

    GENERAL_OPTIONS = ["--syntax-highlight=short", "--smart-quotes=yes"]

    def __init__(self, opts: argparse.Namespace):
        self._src: str = opts.input
        self._verbose: bool = opts.verbose
        self._extensions: str = opts.ext

    def set_theme(self, path: str, name: str) -> None:
        if os.path.exists(name):
            self.theme_dir = os.path.abspath(name)
        else:
            self.theme_dir = os.path.join(path, name)
        print("Using %s" % self.theme_dir)

    def _list_resources(self, origin: str, extension: str) -> list[str]:
        r = []
        for fname in os.listdir(os.path.join(self.theme_dir, origin)):
            if fname.endswith(extension):
                r.append(os.path.join(self.theme_dir, origin, fname))
        r.sort()
        if DEBUG:
            print("List(*%s) = %s" % (extension, ", ".join(r)))
        return r

    def get_output(self, fmt: str) -> str:
        return self._src.rsplit(".", 1)[0] + "." + fmt

    def __execute(self, args: list[str]) -> None | tuple[bytes, bytes]:
        if DEBUG:
            print("Executing %s" % " ".join(args))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        def show_result() -> None:
            print("\nStdout:")
            print(out.decode("utf-8").strip())
            print("\nStderr:")
            print(err.decode("utf-8").strip())

        if proc.returncode == 0:
            if self._verbose:
                show_result()
            return (out, err)
        else:
            print(" PROBLEM! ".center(80, "#"))
            show_result()
            return None

    def make_pdf(self) -> None:
        out = self.get_output("pdf")
        opts = [o for o in self.GENERAL_OPTIONS if "syntax" not in o]
        opts += ["--font-path", os.path.join(self.theme_dir, "fonts")]

        args = [
            "rst2pdf",
            "--fit-background-mode=scale",
            "--use-floating-images",
            "--real-footnotes",
            "-e",
            "preprocess",
        ] + opts
        for style in self._list_resources("pdf", ".yaml"):
            args.extend(("-s", style))
        if self._extensions:
            args.extend(("-e", self._extensions))
        args.extend(("-o", out, self._src))
        if self.__execute(args):
            print(out)

    def make_odt(self) -> None:
        out = self.get_output("odt")
        css = self._list_resources("odt", "odt")[0]
        args = ["rst2odt"] + self.GENERAL_OPTIONS + ["--add-syntax-highlighting", "--stylesheet", css, self._src, out]
        if self.__execute(args):
            print(out)

    def make_html(self) -> None:
        out = self.get_output("html")
        css = ",".join(self._list_resources("html", "css"))
        args = ["rst2html"] + self.GENERAL_OPTIONS + ["--embed-stylesheet", "--stylesheet-path", css, self._src, out]
        if self.__execute(args):
            print(out)
        # post process
        links = os.path.join(self.theme_dir, "html", "links.html")
        if os.path.exists(links):
            data = open(out).read()
            data = data.replace("<html>", "<html>\n" + open(links).read())
            open(out, "w").write(data)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true", help="Display commands' output")

    parser.add_argument(
        "input",
        type=str,
        metavar="FILE",
        nargs="?",
        help="The .rst or .txt file to convert",
    )

    for fmt in SUPPORTED_FORMATS:
        parser.add_argument("--%s" % fmt, action="store_true", help="Generate %s output" % fmt.upper())

    parser.add_argument("-t", "--theme", type=str, default=THEME, help="Use a different theme")

    parser.add_argument(
        "--themes-dir",
        type=str,
        default=THEMES_DIR,
        help="Change the folder searched for theme",
    )

    parser.add_argument("--ext", type=str, default="", help="Load docutils extensions (coma separated)")

    parser.add_argument("-l", "--list", action="store_true", help="List available themes")

    args = parser.parse_args()

    cmd = CommandExecutor(args)
    cmd.set_theme(args.themes_dir, args.theme)

    if args.list:
        for t in os.listdir(THEMES_DIR):
            if t[0] not in "_." and os.path.isdir(os.path.join(THEMES_DIR, t)):
                print(t)
    elif not any(getattr(args, fmt) for fmt in SUPPORTED_FORMATS):
        print("No action ! Give one or more --(%s)" % "|".join(SUPPORTED_FORMATS))
    else:
        if not args.input:
            print("No input file !")
        else:
            for fmt in SUPPORTED_FORMATS:
                if getattr(args, fmt):
                    fn = getattr(cmd, "make_%s" % fmt)
                    print(" %5s:  " % fmt, end="")
                    fn()


if __name__ == "__main__":
    main()
