# -*- coding: utf-8 -*-

"""
The valid serial number ranges of Baxter's products.
"""

# TODO: Refine these ranges

V6_SNs = ((460000, 470000), (720000, 1125000))
V8_SNs = ((2000000, 2300000))
V9_SNs = ((3000000, 3300000))


## Conditions


def V6_SN_check(__sn: int) -> bool:
    return any(lb <= __sn <= ub for lb, ub in V6_SNs)


def V8_SN_check(__sn: int) -> bool:
    return any(lb <= __sn <= ub for lb, ub in V8_SNs)


def V9_SN_check(__sn: int) -> bool:
    return any(lb <= __sn <= ub for lb, ub in V9_SNs)


def global_constraint(__sn: int) -> bool:
    return V6_SN_check(__sn) or V8_SN_check(__sn) or V9_SN_check(__sn)