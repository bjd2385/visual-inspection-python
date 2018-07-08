"""
Walk an Evaluation Technician through a visual inspection of a Spectrum V6, V8, or V9
infusion device using INF 01143-SVC rev. {0} and ITP 35022-SVC rev. {1}.
"""

from .serial_numbers import (V6_SN_check, V8_SN_check, V9_SN_check, 
                             global_constraint, SN_REDUNDANCY)
from .exceptions import InvalidSerialNumberException, SerialNumberMismatchException
from rev import REVISION_INF_01143_SVC, REVISION_ITP_35022_SVC
from .tree import PartsGraph

from typing import Optional, Callable as Function, List, Dict
from abc import ABCMeta, abstractmethod
from enum import Enum
from argparse import ArgumentParser
from logging import Logger
from tkinter import Tk
from functools import wraps
from base64 import b64encode, b64decode

import cmd
import traceback
import logging


## TODO: Implement max logging command queue size for restore
level = logging.INFO
handler = logging.FileHandler('cmds.log')
encoded_handler = logging.FileHandler('cmds_encoded.log')
logger = logging.Logger()


class Version(Enum):
    V6 = 1
    V8 = 2
    V9 = 3


class Category(Enum):
    REPAIR = 1
    RECERT = 2
    RENTAL = 3


def save_data(logger: , prefix: str) -> Function:
    """
    Decorator for cmd.Cmd to save/log data after every valid command.
    """
    def save_data(f: Function) -> Function:
        @functools.wraps(f)
        def new_f(*args, **kwargs):
            res = f(*args, **kwargs)



class Clipboard:
    """
    Context manager to provide a basic interface to tkinter's clipboard
    functionality. (This class provides the program the ability to immediately 
    copy results of the inspection to the clipboard, so an evaluator can paste 
    it into their EN Device Evaluation Assessment.
    """

    def __init__(self, msg: Optional[str] =None) -> None:
        self.msg = msg

    def __enter__(self) -> 'Clipboard':
        self._tk_instance = Tk()
        self._tk_instance.withdraw()
        self._tk_instance.clipboard_clear()
        return self

    def copy(self, msg: Optional[str] =None) -> None:
        if msg is None and self.msg is None:
            return
        elif msg is not None:
            self.msg = msg
            
        self._tk_instance.clipboard_append(self.msg)
        self._tk_instance.update()

    def __exit__(self, exception_type: type, exception_value: Exception,
                 traceback: traceback) -> None:
        self._tk_instance.destroy()


class _BaseCmd(cmd.Cmd):
    """
    Basic features I'd like to add to cmd.Cmd for use in every other command
    line. For instance, the ability to use it as a context manager.
    """
    
    # TODO: Make 
    #def precmd(self, line: str) -> str:
    #    """
    #    Process each line to remove capitalization.
    #    """
    #    return line.lower()

    ## CM support

    def __enter__(self) -> 'SNInput':
        return self

    def __exit__(self, exception_type: type, 
                 exception_value: Exception, traceback: traceback) -> None:
        pass

    ## Add the ability to quit multiple ways

    def do_h(self, line: str) -> None:
        """ 
        List available commands with "help" or detailed help with "help cmd". 
        """
        self.do_help(line)

    def exit(self, line: str) -> None:
        """ Exit the loop """ 
        raise EOFError

    def quit(self, line: str) -> None:
        """ Exit the loop """
        raise EOFError

    ## Additional functionality

    def emptyline(self) -> None:
        """
        Do nothing if nothing is input instead of running the last command.
        """
        pass




class InfusionDevice(metaclass=ABCMeta):
    """
    Base class for visual inspection of Baxter's Spectrum infusion devices.

    note that this class does not inherit from _BaseCmd, but it does define a 
    question queue, which binds the part and processes graph with the questions.
    """
    
    SerialNumber: Optional[int] = None
    DeviceType: Optional[Category] = None

    class QuestionQueue(_BaseCmd):
        """
        Provide functionality for moving forward and backward through questions.
        """
        #queue = PartsGraph()

    def getSN(self, conditions: List[Function[[int], bool]]) -> Optional[int]:
        """
        Check each condition on an input device SN. This is just a basic loop
        """
        while True:
            sns = []
            for _ in range(SN_REDUNDANCY):
                if not sns:
                    sn_in = input('Enter a SN: ')
                else:
                    sn_in = input('Repeat the SN: ')
                if sn_in in ['q', 'quit', 'end']:
                    return
                if not all(condition(sn_in) for condition in conditions):
                    print(f'*** Error: {sn_in} does not satisfy SN conditions'
                           'restarting loop')
        return SN

    @abstractmethod
    def startQuestions(self) -> None:
        raise NotImplementedError


class V6(InfusionDevice, _BaseCmd):
    """
    Represents a Spectrum V6 Infusion device.
    """
    def __init__(self, SN: Optional[int] =None) -> None:
        super(self, InfusionDevice).__init__(self, )
        self.version = Version.V6
        if SN:
            self.SerialNumber = SN
        else:
            self.SerialNumber = self.getSN([V6_SN_check])
            if not self.SerialNumber:


    def startQuestions(self) -> None:
        """
        Start V6 questions.
        """


class V8(InfusionDevice, _BaseCmd):
    """
    Represents a Spectrum V8 Infusion device.
    """
    def __init__(self, SN: Optional[int] =None) -> None:
        raise NotImplementedError('V8 has not been implemented as of yet')


class V9(InfusionDevice, _BaseCmd):
    """
    Represents a Spectrum V9 Infusion device.
    """
    def __init__(self) -> None:
        raise NotImplementedError('V9 has not been implemented as of yet')


class Visual(_BaseCmd):
    """
    Base loop that's instantiated.
    """

    prompt = 'Visual$ '

    def do_V6(self, line: str) -> None:
        """
        Start visual inspection in V6.
        """
        try:
            print('*** Starting V6 visual inspection')
            cmd = V6()
            cmd.cmdloop()
        except NotImplementedError:
            print('V6 Not implemented')

    def do_V8(self, line: str) -> None:
        """
        Start visual inspection in V8. (Not implemented)
        """
        try:
            cmd = V8()
            cmd.cmdloop()
            print('*** Starting V8 visual inspection')
        except NotImplementedError:
            print('V8 Not implemented')

    def do_V9(self, line: str) -> None:
        """
        Start visual inspection in V9. (Not implemented)
        """
        try:
            print('*** Starting V9 visual inspection')
            cmd = V9()
            cmd.cmdloop()
        except NotImplementedError:
            print('V9 Not implemented')


def main() -> None:
    parser = ArgumentParser(
      description=__doc__.format(REVISION_INF_01143_SVC, REVISION_ITP_35022_SVC)
    )

    # TODO: Add debug functionality and logging
    #parser.add_argument('-d', '--debug', action='store_true', default=False,
    #  help='Log output'
    #)

    # TODO: Add restore functionality from logs
    #parser.add_argument('--restore', )

    args = parser.parse_args()

    # Start main interpreter
    with Visual() as cmd:
        cmd.cmdloop()
