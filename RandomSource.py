#  Copyright (c) 2021. Alexander Hermes
from collections import defaultdict
from random import randrange

from Changeset import Changeset


class RandomSource:
    """
    Source for randomly generated instances of :class:`Changeset`
    """
    ARRIVAL_RANGE = (1, 720)
    COMPILE_RANGE = (60, 120)
    TEST_RANGE = (120, 360)

    def __init__(self, num: int):
        self.pool = self.gen_changesets(num)

    def draw(self, tick: int) -> list[Changeset]:
        """
        Draw the change sets that have arrived at the given tick time
        :param tick: tick time used to draw sets
        :return: the change sets that have deemed to have arrived at the given time
        """
        return self.pool.pop(tick, [])

    def empty(self) -> bool:
        """
        Whether or not this source is exhausted (has no more changesets).
        """
        return len(self.pool) == 0

    @staticmethod
    def gen_changesets(num: int) -> dict[int, list[Changeset]]:
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
            c = Changeset(
                compile_duration=randrange(RandomSource.COMPILE_RANGE[0], RandomSource.COMPILE_RANGE[1]),
                test_duration=randrange(RandomSource.TEST_RANGE[0], RandomSource.TEST_RANGE[1]),
                changed_modules=[]  # ignored for the time being
            )
            pool[t].append(c)

        return pool
