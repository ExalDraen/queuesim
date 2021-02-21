#  Copyright (c) 2021. Alexander Hermes
from dataclasses import dataclass
from enum import Enum

from Changeset import Changeset


class Phase(Enum):
    WAITING = 0
    COMPILING = 1
    TESTING = 2
    DONE = 3
    RELEASED = 4
    UNKNOWN = 5


@dataclass
class Release:
    name: str
    changeset: Changeset
    queued_time: int
    compile_start: int = 0
    compile_end: int = 0
    test_start: int = 0
    test_end: int = 0
    released_time: int = 0

    def phase(self) -> Phase:
        if self.compile_start == 0:
            return Phase.WAITING
        elif self.compile_start != 0 and self.compile_end == 0:
            return Phase.COMPILING
        elif self.test_start != 0 and self.test_end == 0:
            return Phase.TESTING
        elif self.test_end != 0:
            return Phase.DONE
        elif self.released_time != 0:
            return Phase.RELEASED
        else:
            return Phase.UNKNOWN

    def is_done(self) -> bool:
        return self.phase() == Phase.DONE

    def mark_released(self, tick: int):
        """
        Mark release as released at the tick time provided
        """
        self.released_time = tick

    def process_tick(self, tick: int):
        # If we're waiting, start compilation
        if self.phase() == Phase.WAITING:
            self.compile_start = tick
        # If we're compiling, check if we're done with that
        # and can start testing
        elif self.phase() == Phase.COMPILING:
            if tick >= self.compile_start + self.changeset.compile_duration:
                self.compile_end = tick
                self.test_start = tick
        # And if we're testing, see if we're done with that and can
        # declare victory
        elif self.phase() == Phase.TESTING:
            if tick >= self.test_start + self.changeset.test_duration:
                self.test_end = tick
        # Otherwise, nothing to do
