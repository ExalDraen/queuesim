#  Copyright (c) 2021. Alexander Hermes
import random
import uuid
from collections import defaultdict
from random import randrange

from Changeset import Changeset, Module


class RandomSource:
    """
    Source for randomly generated instances of :class:`Changeset`
    """
    ARRIVAL_RANGE = (1, 720)
    COMPILE_RANGE = (60, 120)
    TEST_RANGE = (120, 360)
    NUM_MODULES_RANGE = (10, 40)  # Total number of modules in existence
    MODULES_RANGE = (1, 5)  # Number of modules in a changeset

    # Quick type for pool from which random data is drawn
    Pool = dict[int, list[Changeset]]
    ModulePool = set[Module]

    def __init__(self):
        # Module pool must be initialized before changeset pool
        self.module_pool = self.gen_modules()
        self.pool = {}

    def initialize(self, num: int):
        self.pool = self.gen_changesets(num)

    def initialize_from(self, pool: Pool):
        self.pool = pool

    def draw(self, tick: int) -> list[Changeset]:
        """
        Draw the change sets that have arrived at the given tick time
        :param tick: tick time used to draw sets
        :return: the change sets that have been deemed to have arrived at the given time
        """
        return self.pool.pop(tick, [])

    def empty(self) -> bool:
        """
        Whether or not this source is exhausted (has no more changesets).
        """
        return len(self.pool) == 0

    def gen_changesets(self, num: int) -> Pool:
        """
        Randomly generate changesets and arrival times and return them

        :param num: number of changesets to generate
        :return: Map of arrival time: list of changesets that arrive
        at this time
        """
        pool = defaultdict(list)

        # Randomly generate the requested number of change sets, keyed
        # by arrival time
        for i in range(num):
            t = randrange(RandomSource.ARRIVAL_RANGE[0], RandomSource.ARRIVAL_RANGE[1])
            # TODO: The test modules should be derived from the change modules
            c = Changeset(
                changed_modules=self.draw_modules(
                    random.randrange(RandomSource.MODULES_RANGE[0], RandomSource.MODULES_RANGE[1])),
                modules_to_test=self.draw_modules(
                    random.randrange(RandomSource.MODULES_RANGE[0], RandomSource.MODULES_RANGE[1])),
            )
            pool[t].append(c)

        return pool

    @staticmethod
    def gen_modules() -> ModulePool:
        """
        Generate a random pool of changeset modules (instances of :class:`Module`)

        :return: pool of changeset modules
        """
        num = random.randrange(RandomSource.NUM_MODULES_RANGE[0], RandomSource.NUM_MODULES_RANGE[1])
        pool = set()
        for i in range(num):
            m = Module(
                name=f"mod-{i}",
                compile_duration=random.randrange(RandomSource.COMPILE_RANGE[0], RandomSource.COMPILE_RANGE[1]),
                test_duration=random.randrange(RandomSource.TEST_RANGE[0], RandomSource.TEST_RANGE[1]),
            )
            pool.add(m)
        return pool

    def draw_modules(self, num: int) -> set[Module]:
        """
        Return a set of modules randomly drawn from the module pool

        :param num: The number of modules to draw
        """
        return set(random.sample(list(self.module_pool), num))
