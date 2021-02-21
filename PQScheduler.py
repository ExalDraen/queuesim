#  Copyright (c) 2021. Alexander Hermes
import logging
import uuid
from collections import deque

from Changeset import Changeset
from Release import Release

logger = logging.getLogger(__name__)


class PQScheduler:
    """
    Scheduler with a single queue but where queued requests can progress
    in parallel with the front of the queue (but ot exit the queue).

    That is, requests are serviced in parallel but only released on at a time
    """

    def __init__(self):
        self.active_q: deque[Release] = deque()  # represents FIFO queue
        self.done_q: list[Release] = list()
        self.tick: int = 0  # Simulation tick

    def accept_changeset(self, cs: Changeset):
        # This scheduler runs changesets in parallel, but only releases from the front
        # This means that new changesets must contain all of the changes contained
        # in changesets that are already queued. Therefore, we need to compile the
        # union of all the changed modules
        # However, we don't need to union the tests modules as we only need to validate the
        # new changes (previous changes were validated by previous changesets).
        mod_cs = Changeset(
            changed_modules=set.union(cs.changed_modules, *(r.changeset.changed_modules for r in self.active_q)),
            modules_to_test=cs.modules_to_test
        )
        logger.debug("Incoming changeset: %s, queued changeset: %s", cs, mod_cs)
        r = Release(name=f"R-{uuid.uuid4().hex}", changeset=mod_cs, queued_time=self.tick)
        self.active_q.append(r)

    def process_tick(self, new_tick: int):
        self.tick = new_tick
        if len(self.active_q) <= 0:
            logger.debug("Processing requested, but queue empty, nothing to do")
            return

        # All of the releases in the queue get to progress
        for r in self.active_q:
            r.process_tick(new_tick)

        # But only the front of the queue gets to release
        current = self.active_q[0]
        if current.is_done():
            logger.info("Release %s complete, moving to done list", current)
            current.mark_released(new_tick)
            self.done_q.append(self.active_q.popleft())

        logger.debug("Processed tick %s. Remaining active requests: %s, Done: %s",
                     new_tick, len(self.active_q), len(self.done_q))

    def idle(self):
        """
        Whether or not this scheduler is doing anything

        :return: true if scheduler is idle (no active requests), false otherwise
        """
        return len(self.active_q) == 0

    def get_results(self) -> list[Release]:
        return self.done_q

