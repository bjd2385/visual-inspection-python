#! -*- coding: utf-8 -*-

"""
Test whether the visual inspection questions form an onto-mapping with the parts
list, i.e. Questions : PartsList -> PartsList is an onto mapping.
"""

from ..scripts.cmdline import get_data

import unittest


class TestOnto(unittest.TestCase):
    __doc__ = __doc__

    def setUp(self) -> None:
        self.data = get_data()

    def test_onto(self) -> None:
        ...