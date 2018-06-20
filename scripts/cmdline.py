#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
Walk an Evaluation Technician through a visual inspection of a Spectrum V6, V8, or V9
infusion device.
"""

from .serial_numbers import V6_SN_check, V8_SN_check, V9_SN_check
from .exceptions import InvalidSerialNumberException, SerialNumberMismatchException
from ..rev import REVISION_INF_01143_SVC, REVISION_ITP_35022_SVC

from typing import Optional, Callable as Function, List
from abc import ABCMeta
from enum import Enum
from argparse import ArgumentParser
from logging import Logger

import cmd
import json
import datetime


def getINF01143_SVC_data(fname: str ='data/visual_inspection.json') -> str:
    """
    Parse JSON data about parts and processes on the INF 01143-SVC and INF 01143-CFG2-SVC.
    """
    with open(fname, 'r') as data:
        lines = data.read()

    decoder = json.JSONDecoder()
    decoded = decoder.decode(lines)

    # update opening statement to a lambda function pending the device's SN.
    decoded['opening'] = lambda sn: decoded['opening'].format(
        datetime.date.today().strftime('%B %d, %Y,'),
        sn,
        REVISION_ITP_35022_SVC
    )

    return decoded


class Version(Enum):
    V6 = 1
    V8 = 2
    V9 = 3


class Category(Enum):
    REPAIR = 1
    RECERT = 2
    RENTAL = 3


class InfusionDevice(metaclass=ABCMeta):
    """
    Base class for Baxter's Spectrum infusion devices.
    """
    SerialNumber: Optional[int] = None
    DeviceType: Optional[Category] = None

    class SNInput(cmd.Cmd):
        """
        Get proper SN input.
        """
        prompt = 'SN: '
        inputSNs = []

        def cmdloop(self, intro: Optional[str] =None) -> int:
            """
            Overridden cmd.Cmd `cmdloop` method. Most of this is the same, but I've
            re-written the loop to halt and return the first serial number of
            `self.inputSNs`.
            """
            self.preloop()
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    self.old_completer = readline.get_completer()
                    readline.set_completer(self.complete)
                    readline.parse_and_bind(self.completekey + ": complete")
                except ImportError:
                    pass
            try:
                if intro is not None:
                    self.intro = intro
                if self.intro:
                    self.stdout.write(str(self.intro) + "\n")
                while True:
                    if self.cmdqueue:
                        line = self.cmdqueue.pop(0)
                    else:
                        if self.use_rawinput:
                            try:
                                line = input(self.prompt)
                            except EOFError:
                                line = 'EOF'
                        else:
                            self.stdout.write(self.prompt)
                            self.stdout.flush()
                            line = self.stdin.readline()
                            if not len(line):
                                line = 'EOF'
                            else:
                                line = line.rstrip('\r\n')
                    line = self.precmd(line)
                self.postloop()
                return self.inputSNs[0]
            finally:
                if self.use_rawinput and self.completekey:
                    try:
                        import readline
                        readline.set_completer(self.old_completer)
                    except ImportError:
                        pass


    def getSN(self, conditions: List[Function[[int], bool]]) -> int:
        """
        Check each condition on an input device SN.
        """
        SN = self.SNInput().cmdloop(intro='Enter the device serial number')
        return SN


    @staticmethod
    def trimParts():
        """
        Recursively update/trim required parts and processes based on included/collaterals.

        To be called after every "yes" answer.
        """



class V6(InfusionDevice, cmd.Cmd):
    """
    Represents a Spectrum V6 Infusion device.
    """
    def __init__(self, SN: Optional[int] =None) -> None:
        super(V6, )
        self.version = Version.V6
        if SN:
            self.SerialNumber = SN
        else:
            self.SerialNumber = self.getSN([V6_SN_check])





class V8(InfusionDevice, cmd.Cmd):
    """
    Represents a Spectrum V8 Infusion device.
    """
    def __init__(self, SN: Optional[int] =None) -> None:
        self.version = Version.V8
        if SN:
            self.SerialNumber = SN
        else:
            self.SerialNumber = self.getSN([V8_SN_check])


class V9(InfusionDevice, cmd.Cmd):
    """
    Represents a Spectrum V9 Infusion device.
    """
    def __init__(self) -> None:
        raise NotImplementedError('V9 has not been implemented as of yet')


class Visual(cmd.Cmd):
    """
    Main interpreter class.
    """

    prompt = 'Visual$ '

    def do_h(self, line: str) -> None:
        self.do_help(line)

    def exit(self, line: str) -> None:
        raise EOFError

    def help_exit(self) -> None:


    def quit(self, line: str) -> None:
        raise EOFError

    def do_V6(self, line: str) -> None:
        """
        Start visual inspection in V6.
        """
        try:
            print('*** Starting V6 visual inspection')
            cmd = V6()
            cmd.cmdloop()
        except NotImplementedError:
            self.default('')

    def do_V8(self, line: str) -> None:
        """
        Start visual inspection in V8.
        """
        try:
            print('*** Starting V8 visual inspection')
            cmd = V8()
            cmd.cmdloop()
        except NotImplementedError:
            self.default('')

    def do_V9(self, line: str) -> None:
        """
        Start visual inspection in V9.
        """
        try:
            print('*** Starting V9 visual inspection')
            cmd = V9()
            cmd.cmdloop()
        except NotImplementedError:
            self.default('')


def main() -> None:
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('-d', '--debug', action='store_true', default=True,
        help='Log output'
    )

    #parser.add_argument('--restore', )

    args = parser.parse_args()

    # Start main interpreter
    Visual().cmdloop()