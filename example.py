#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Brandon Doyle <bjd2385@aperiodicity.com>
#
# Distributed under terms of the MIT license.

"""

"""

import cmd


class Visual(cmd.Cmd):
    """ simple cmd line example """

    prompt = 'Visual$ '

    def do_h(self, line: str) -> None:
        self.do_help(line)

    def do_greet(self, line) -> None:
        print('hello')

    def do_EOF(self, line) -> bool:
        return True

    def postloop(self) -> None:
        print()


if __name__ == '__main__':
    Visual().cmdloop()
