#! -*- coding: utf-8 -*-

"""
Parts tree. Much like a variable `n`-ary tree.
"""

from typing import Dict, List, Callable as Function


# Lookup structure that `PartsTree` uses reason about trim and collaterals
Structure = Dict[
    str,
    List[str,
         str,
         Dict[str, List[str]],
         Dict[str, List[str]],
         Dict[str, List[str]]
    ]
]


class PartsTree:
    """
    Our `n`-ary tree (functor) implementation, with methods for adding collaterals
    and trimming included parts therein.
    """

    pts_processes: List[str] = []   # final parts/processes list for pasting

    def __init__(self, parts: Structure) -> None:
        ...

    def fmap(self, fn: Function[[], ...]) -> 'PartsTree':
        """
        Map a function across the tree.


        """