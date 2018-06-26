# -*- coding: utf-8 -*-

"""
Test whether the visual inspection questions form an onto-mapping with the parts
list, i.e. Questions : PartsList -> PartsList is an onto mapping.
"""

from ..scripts.tree import get_data, Structure, Questions

import unittest

__all__ = [
    'TestOnto'
]


class TestOnto(unittest.TestCase):
    """
    Ensure that a questions list contained in data/visual_inspection.json can be
    mapped onto the complete set of parts. More mathematically,

    ∀pϵParts, ∃qϵQuestions s. th. F(q) -> p.

    This test is F.
    """

    _TOTAL_PROCESSES = set()
    _TOTAL_PARTS = set()

    def setUp(self) -> None:
        self.data = get_data()
        self.parts: Structure = self.data['V6Parts']
        self.questions: Questions = self.data['questions']

        self.len_parts = len(self.parts)

    def test_onto(self) -> None:
        for level in self.questions:
            for question in level:
                print(question)
                #self._TOTAL_PARTS | question[]