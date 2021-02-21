#  Copyright (c) 2021. Alexander Hermes
from dataclasses import dataclass


@dataclass
class Changeset:
    """
    Represents a change set (patch to existing code) and the time
    it would take to compile & test
    """
    compile_duration: int
    test_duration: int
    changed_modules: list[str]
