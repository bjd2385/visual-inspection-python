"""
Test the clipboard functionality.
"""

from scripts.cmdline import Clipboard

import unittest


class TestClipboard(unittest.TestCase):
    """
    Test the Clipboard functionality.
    """

    def setUp(self) -> None:
        with Clipboard() as cb:
            self.clipboard = cb
