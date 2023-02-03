"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import logging

from colorama import init, Fore, Back, Style


__all__ = ('Handler', 'Formatter')


init(autoreset=True)
LEVEL_COLOURS = {
    'CRITICAL': {'highlight': Back.RED, 'base': Fore.RED},
    'ERROR': {'highlight': Back.RED, 'base': Fore.RED},
    'WARNING': {'highlight': Back.YELLOW, 'base': Fore.YELLOW},
    'INFO': {'highlight': Back.BLUE, 'base': Fore.LIGHTBLUE_EX},
    'DEBUG': {'highlight': Back.GREEN, 'base': Fore.LIGHTGREEN_EX}
}


class Formatter:

    def colour_format(self, record: logging.LogRecord) -> str:
        colours: dict[str, str] = LEVEL_COLOURS[record.levelname]

        name_back = Back.MAGENTA if record.name.startswith('core') else Back.BLACK
        name_fore = Fore.BLACK if record.name.startswith('core') else Fore.WHITE

        fmt: str = Back.BLACK + \
                   '[{asctime}] ' + \
                   Back.RESET + \
                   colours['highlight'] + \
                   Fore.BLACK + \
                   '[{levelname:<8}]' + \
                   name_back + \
                   name_fore + \
                   ' {name:<20}' + \
                   Back.RESET + \
                   colours['base'] + \
                   ': {message}'

        formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S', style='{')
        return formatter.format(record)

    def format(self, record: logging.LogRecord) -> str:
        fmt: str = '[{asctime}] [{levelname:<8}] {name:<20}: {message}'

        formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S', style='{')
        return formatter.format(record)


class Handler(logging.Handler):

    def __init__(self, level: int) -> None:
        super().__init__()

        self._level = level
        self._formatter: Formatter = Formatter()

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= self._level:
            print(self._formatter.colour_format(record))

        self.flush()
