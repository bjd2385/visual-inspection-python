#! -*- coding: utf-8 -*-

"""
Test whether the visual inspection questions form an onto-mapping with the parts
list, i.e. Questions : PartsList -> PartsList is an onto mapping.
"""

from ..scripts.tree import get_data

import unittest


class TestOnto(unittest.TestCase):
    """
    Test
    """

    def setUp(self) -> None:
        self.data = get_data()
        self.parts = self.data['parts']

    def test_onto(self) -> None:
        ...