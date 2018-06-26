#! -*- coding: utf-8 -*-

"""
Parts data graph.
"""

from rev import REVISION_INF_01143_SVC, REVISION_ITP_35022_SVC

from typing import Dict, List, Callable as Function, Tuple, Optional, Union
from collections.abc import Iterator
from itertools import zip_longest

import json
import datetime
import traceback


# High leve view of the structure of each parts list
Structure = Dict[str, List[Union[str, str, Dict[str, List[str]], Dict[str, List[str]]]]]

# Structure of questions in JSON file
Questions = Dict[str, Dict[str, Dict[str, List[str]]]]


def get_data(fname: str ='data/visual_inspection.json') -> Dict:
    """
    Parse JSON data about parts and processes on the INF 01143-*SVC.
    """
    with open(fname, 'r') as data:
        lines = data.read()

    decoder = json.JSONDecoder()
    decoded = decoder.decode(lines)

    # update statements to a lambda function pending the device's SN.
    for key in ('opening', 'default'):
        decoded[key] = lambda sn: decoded[key].format(
            datetime.date.today().strftime(r'%B %d, %Y,'),
            sn,
            REVISION_ITP_35022_SVC
        )

    return decoded


class GraphNode(Iterator):
    """
    Maintain part information and connections/relations to other parts.

    Each node is also iterable, so you can iterate over the collateral and included
    parts, as well as the included processes, all at the same time.
    """
    collaterals: Tuple['GraphNode'] = ()
    inclParts: Tuple['GraphNode'] = ()

    # because nodes are based on PNs, processes are collateral information
    inclProcs: Tuple[str] = ()

    def __init__(self, partN: str) -> None:
        self.partN = partN
        self.__state = 0
        self.__max = 0

    def __eq__(self, other: 'GraphNode') -> bool:
        return self.partN == other.partN

    def __enter__(self) -> 'GraphNode':
        return self

    def _getMaxLength(self) -> int:
        return max(map(len, (self.collaterals, self.inclParts, self.inclProcs)))

    def setCltrl(self, collaterals: Tuple['GraphNode'] =()) -> 'GraphNode':
        self.collaterals = collaterals
        if self.__state == 0:
            self.__max = self._getMaxLength()
        return self

    def setInclPts(self, includedParts: Tuple['GraphNode'] =()) -> 'GraphNode':
        self.includedParts = includedParts
        if self.__state == 0:
            self.__max = self._getMaxLength()
        return self

    def setInclProc(self, includedProcesses: Tuple['GraphNode'] =()) -> 'GraphNode':
        self.includedProcesses = includedProcesses
        if self.__state == 0:
            self.__max = self._getMaxLength()
        return self

    def __iter__(self) -> 'GraphNode':
        self.__state = 0
        self.__levels = zip_longest(
            self.collaterals,
            self.includedParts,
            self.includedProcesses
        )
        return self

    tpType = Optional[Tuple['GraphNode']]

    def __next__(self) -> Tuple[tpType, tpType, Optional[Tuple[str]]]:
        if self.__state >= self.__max:
            raise StopIteration
        val = self.__levels[self.__state]
        self.__state += 1
        return val

    def __exit__(self, exception_type: type, exception_value: Exception,
                 traceback: traceback) -> None:
        pass


class PartsGraph:
    """
    Maintain a parts tree.
    """
    def __init__(self, parts: Structure, processes: Dict[str, List[str]]) -> None:
        self.parts = parts
        self.processes = processes

