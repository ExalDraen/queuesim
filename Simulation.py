#  Copyright (c) 2021. Alexander Hermes
import logging
import time

from Changeset import Changeset
from SQScheduler import SQScheduler

logger = logging.getLogger(__name__)


class Simulation:
    SLEEP_SECS: float = 0.0001

    def __init__(self, source, scheduler: SQScheduler):
        self.tick: int = 0
        self.source = source  # Source of changesets
        self.scheduler = scheduler

    def run(self):
        """
        Run simulation until there's nothing left to simulate
        """
        while not self.is_complete():
            self.advance()
            time.sleep(Simulation.SLEEP_SECS)

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
        print(self.scheduler.get_results())