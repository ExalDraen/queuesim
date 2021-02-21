#  Copyright (c) 2021. Alexander Hermes
import logging
import time
from typing import Union

from Changeset import Changeset
from PQScheduler import PQScheduler
from RandomSource import RandomSource
from SQScheduler import SQScheduler

logger = logging.getLogger(__name__)


class Simulation:
    SLEEP_SECS: float = 0.0001

    def __init__(self, source: RandomSource, scheduler: Union[SQScheduler, PQScheduler]):
        self.tick: int = 0
        self.source = source  # Source of changesets
        self.scheduler = scheduler

    def run(self):
        """
        Run simulation until there's nothing left to simulate
        """
        while not self.is_complete():
            self.advance()
            # time.sleep(Simulation.SLEEP_SECS)

    def advance(self):
        """
        Advance world state by 1 tick
        """
        logger.debug("Advancing world state %s -> %s", self.tick, self.tick + 1)
        # Draw change sets from source
        new_cs: list[Changeset] = self.source.draw(self.tick)

        # Add them to queue
        for c in new_cs:
            self.scheduler.accept_changeset(c)

        # Do processing
        self.scheduler.process_tick(self.tick)

        # Advance time
        self.tick = self.tick + 1

    def is_complete(self) -> bool:
        """
        Whether or not the simulation has nothing left to do
        :return: true if there is nothing further to simulate, false otherwise
        """
        return self.source.empty() and self.scheduler.idle()

    def output_results(self):
        """
        Print current results of simulation
        """
        outputs = self.scheduler.get_results()
        total_compile_time = sum((x.compile_end - x.compile_start for x in outputs))
        total_test_time = sum((x.test_end - x.test_start for x in outputs))
        last_release = max((x.released_time for x in outputs))
        print(f"\n\n***** RESULTS  for {self.scheduler.__class__} *****\n")
        print("*** INPUTS")
        print(f"Arrival time range: {self.source.ARRIVAL_RANGE}")
        print(f"Compile time range: {self.source.COMPILE_RANGE}")
        print(f"Test time range: {self.source.TEST_RANGE}")
        print(f"{self.source.NUM_MODULES_RANGE=}")
        print(f"{self.source.MODULES_RANGE=}")
        print(f"Total module pool size: {len(self.source.module_pool)}")

        print("\n*** OUTPUTS")
        print(f"Last release at: {last_release}")
        print(f"Total Compile time: {total_compile_time}")
        print(f"Total Test time: {total_test_time}")
        print(outputs)
