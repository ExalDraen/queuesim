#  Copyright (c) 2021. Alexander Hermes
from dataclasses import dataclass


@dataclass
class Module:
    """
    Represents a single module to be built & tested
    """
    name: str
    compile_duration: int
    test_duration: int

    def __hash__(self) -> int:
        return self.name.__hash__()


@dataclass
class Changeset:
    """
    Represents a change set (patch to existing code) and the time
    it would take to compile & test
    """
    changed_modules: set[Module]
    modules_to_test: set[Module]

    @property
    def compile_duration(self) -> int:
        return sum(m.compile_duration for m in self.changed_modules)

    @property
    def test_duration(self) -> int:
        return sum(m.test_duration for m in self.modules_to_test)
