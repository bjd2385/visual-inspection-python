# -*- coding: utf-8 -*-

"""
Test whether the visual inspection questions form an onto-mapping with the parts
list, i.e. Questions : PartsList -> PartsList is an onto mapping.
"""

from scripts.tree import get_data, Structure, Questions
from warnings import warn

import unittest


class TestOnto(unittest.TestCase):
    """
    Ensure that a questions list contained in data/visual_inspection.json can be
    mapped onto the complete set of parts. More mathematically,

    ∀pϵParts, ∃qϵQuestions s. th. F(q) -> p.

    This test is F.
    """

    _processes_mapped_to = set()
    _parts_mapped_to = set()

    def setUp(self) -> None:
        self.data = get_data()
        self.parts = self.data['V6Parts']
        self.part_numbers_set = set(self.parts.keys())
        self.questions = self.data['questions']

        self.len_parts = len(self.parts)

    def test_onto(self) -> None:
        # Get the set of parts mapped to
        for level in self.questions.values():
            for question in level.values():
                self._parts_mapped_to |= set(question['parts'])
        self._parts_mapped_to.discard('')

        # Add all collateral parts (these have a different meaning than in the tree
        # datastructure, where collateral parts are trimmed. I iterate
        # `self.len_parts` times here because it's guaranteed to catch all
        # collateral parts.
        for i in range(self.len_parts):
            collateralParts = set()
            for part in self._parts_mapped_to:
                collateralParts |= set(self.parts[part][2]['collateralParts'])
            self._parts_mapped_to |= collateralParts

        # Get the set of processes mapped to
        for level in self.questions.values():
            for question in level.values():
                self._processes_mapped_to |= set(question['processes'])
        self._processes_mapped_to.discard('')

        warn(f'These parts aren\'t in the image: '
             f'{self.part_numbers_set - self._parts_mapped_to}')

        self.assertEqual(self.len_parts, len(self._parts_mapped_to),
            msg='Questions must cover every part in the provided parts list')