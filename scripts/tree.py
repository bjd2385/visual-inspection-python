#! -*- coding: utf-8 -*-

"""
Parts graph.
"""

from rev import REVISION_INF_01143_SVC, REVISION_ITP_35022_SVC

from typing import Dict, List, Tuple, Optional, Union
from collections.abc import Iterator
from itertools import zip_longest

import json
import datetime
import traceback


# High leve view of the structure of each part entry
Structure = Dict[str, List[Union[str, Dict[str, List[str]]]]]

# Structure of questions in JSON file
Questions = Dict[str, Dict[str, Dict[str, List[str]]]]

_opNode = Optional['GraphNode']


def get_data(fname: str ='data/visual_inspection.json') -> Dict:
    """
    Parse JSON data about parts and processes on the INF 01143-*SVC.
    """
    with open(fname, 'r') as data:
        lines = data.read()

    decoder = json.JSONDecoder()
    decoded = decoder.decode(lines)

    # update statements to a lambda function pending the device's SN. This also
    # ensures that users on second shift writing assessments after midnight see a
    # date change.
    for key in ('opening', 'default'):
        decoded[key] = lambda sn: decoded[key].format(
            datetime.date.today().strftime(r'%B %d, %Y,'),
            sn,
            REVISION_ITP_35022_SVC
        )

    return decoded


class ProcessNode(Iterator):
    """
    Maintain process information and connections/relations to other processes.
    """


class GraphNode(Iterator):
    """
    Maintain part information and connections/relations to other parts.

    Each node is also iterable, so you can iterate over the collateral and included
    parts, as well as the included processes, all at the same time. This flattens
    the iteration to a single loop.
    """
    collaterals: Tuple['GraphNode'] = ()
    inclParts: Tuple['GraphNode'] = ()

    # because nodes are based on PNs, processes are collateral information
    inclProcs: Tuple[str] = ()

    level: str = ''   # level of part ('custom', '1', '2', '3')

    __state: int = 0
    __max: int = 0

    def __init__(self, part_number: str, part_name: str, level: int) -> None:
        self.part_number = part_number
        self.part_name = part_name
        self.level = level

    def __eq__(self, other: 'GraphNode') -> bool:
        return self.part_number == other.part_number

    def __enter__(self) -> 'GraphNode':
        return self

    def __exit__(self, exception_type: type, exception_value: Exception,
                 traceback: traceback) -> None:
        pass

    def _getMaxLength(self) -> int:
        return max(map(len, (self.collaterals, self.inclParts, self.inclProcs)))

    @classmethod
    def encodePart(cls, part_number: str,
                   inf: List[Union[str, Dict[str, List[str]]]]) -> 'GraphNode':
        """
        Set up a node from input data, rather than calling these methods externally.
        """
        part_name, level, relations = inf
        included_parts, collateral_parts, included_processes = relations.items()
        node = cls(part_number, part_name, level)
        node.setInclPts(included_parts)
        node.setCltrl(collateral_parts)
        node.setInclProc(included_processes)
        return node

    def setCltrl(self, collaterals: Tuple['GraphNode'] =()) -> 'GraphNode':
        """
        Set collateral parts tuple.
        """
        self.collaterals = collaterals
        # Setting parts resets state
        if not self.__state:
            self.__max = self._getMaxLength()
        return self

    def setInclPts(self, includedParts: Tuple['GraphNode'] =()) -> 'GraphNode':
        """
        Set included parts tuple.
        """
        self.includedParts = includedParts
        if not self.__state:
            self.__max = self._getMaxLength()
        return self

    def setInclProc(self, includedProcesses: Tuple['GraphNode'] =()) -> 'GraphNode':
        """
        Set included (redundant) processes tuple.
        """
        self.includedProcesses = includedProcesses
        if not self.__state:
            self.__max = self._getMaxLength()
        return self

    def __iter__(self) -> 'GraphNode':
        if self.__state:
            self.__state = 0
        self.__levels = zip_longest(
            self.collaterals,
            self.includedParts,
            self.includedProcesses
        )
        return self

    def __next__(self) -> Tuple[Tuple[_opNode, _opNode, Optional[str]]]:
        if self.__state >= self.__max:
            raise StopIteration
        val = self.__levels[self.__state]
        self.__state += 1
        return val


class PartsGraph:
    """
    Maintain a (possibly cyclic) parts graph.
    """

    _parts = []

    def __init__(self, parts: Structure, processes: Dict[str, List[str]]) -> None:
        self.parts = parts
        self.processes = processes

    def build(self) -> None:
        ...

    def __iter__(self) -> 'PartsGraph':
        return self

    def __next__(self) -> GraphNode:
        ...