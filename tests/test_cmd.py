"""
Test classes in cmdline.py that implement the cmd.Cmd class.
"""

from scripts.cmdline import Visual

import unittest


class TestCmd(unittest.TestCase):

    def setUp(self) -> None:
        self.instance = Visual()

    def test_start(self) -> None:
        self.instance.cmdloop()
