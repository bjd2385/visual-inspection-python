# -*- coding: utf-8 -*-

"""
Test whether the visual inspection questions form a covering of the parts list. I.e.
Questions : Parts -> Parts is onto.
"""

from scripts.tree import get_data

from warnings import warn
from typing import List, Optional, Generator, Tuple
from itertools import zip_longest

import unittest


class TestOnto(unittest.TestCase):
    """
    Ensure that a questions list contained in data/visual_inspection.json can be
    mapped onto the complete set of parts. More mathematically,

    ∀pϵParts, ∃qϵQuestions s. th. F(q) -> p.

    This test is the mapping F. Note that it doesn't have to be a function or 1-1.
    """

    _processes_mapped_to: List[str]
    _parts_mapped_to: List[str]

    def setUp(self) -> None:
        self.data = get_data()

        self.parts = self.data['V6Parts']

        self.part_numbers_set = set(self.parts.keys())
        self.questions = self.data['questions']
        self.processes = self.data['processes']

        self.len_parts = len(self.parts)
        self.len_processes = len(self.processes)

    def flattened_questions(self) -> Generator[Tuple[List[str], List[str]], None, None]:
        """
        Flatten questions for easy iterator.

        Yield parts and processes associated with each question.
        """
        for level in self.questions:
            for question in self.questions[level]:
                yield zip_longest(self.questions[level][question]['parts'],
                                  self.questions[level][question]['processes'])

    def test_in_list(self) -> None:
        """
        Ensure every part required by questions is in the parts list.
        """
        for part, proc in self.flattened_questions():
            if part:
                self.assertIn(part, self.part_numbers_set,
                    msg=f'Part {part} not in parts list')
            if proc:
                self.assertIn(proc, self.processes,
                    msg=f'Process {proc} not in processes list')

    def test_onto_parts(self) -> None:
        """
        Ensure the parts are mapped onto.
        """

        parts = []
        processes = []

        def compile_parts(part: str, proc: Optional[str] =None) -> None:
            """
            Recursively build/traverse a parts and processes list. This function
            is nested further in scripts.tree.py.
            """
            nonlocal parts, processes
            if not parts:
                parts = [part]
            if not proc:
                processes = []
            curr_included_parts: List[str] = self.parts[part][2]['includedParts']
            curr_collaterals: List[str] = self.parts[part][2]['collateralParts']
            curr_included_proc: List[str] = self.parts[part][2]['includedProcesses']
            for _part in curr_included_parts:
                if _part in parts:
                    parts.remove(_part)
            for _part in curr_collaterals:
                if _part not in parts:
                    parts.append(_part)
            for _proc in curr_included_proc:
                if _proc in processes:
                    processes.remove(_proc)

            # Recursively traverse and update
            for _part in parts:
                compile_parts(_part)

        for _parts, _procs in self.flattened_questions():
            for part in _parts:
                compile_parts(part)
            for proc in _procs:
                compile_parts(proc)

        print(parts)
        print(processes)

        exit(0)

        warn(f'These parts aren\'t in the image: '
             f'{self.part_numbers_set - set(self._parts_mapped_to)}', RuntimeWarning)

        self.assertEqual(self.len_parts, len(self._parts_mapped_to),
            msg='Questions must cover every part in the provided parts list')

    def test_onto_processes(self) -> None:
        """
        Ensure the processes are mapped onto.
        """



        warn(f'These processes are not utilized: '
             f'{self.processes - self._processes_mapped_to}')

        self.assertEqual(self.len_processes, len(self._processes_mapped_to),
            msg='Processes are not all mapped to')