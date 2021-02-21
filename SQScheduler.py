#  Copyright (c) 2021. Alexander Hermes
import logging
import uuid
from collections import deque

from Changeset import Changeset
from Release import Release

logger = logging.getLogger(__name__)


class SQScheduler:
    """
    Single queue, naive scheduler.
    """

    def __init__(self):
        self.active_q: deque[Release] = deque()  # represents FIFO queue
        self.done_q: list[Release] = list()
        self.tick: int = 0  # Simulation tick

    def accept_changeset(self, cs: Changeset):
        logger.debug("Accepting changeset: %s", cs)
        r = Release(name=f"R-{uuid.uuid4().hex}", changeset=cs, queued_time=self.tick)
        self.active_q.append(r)

    def process_tick(self, new_tick: int):
        if len(self.active_q) <= 0:
            # Nothing in queue, nothing to do
            logger.info("Active queue empty, nothing to do")
            return

        # Only the release at the front gets to progress
        current: Release = self.active_q[0]
        current.process_tick(new_tick)
        # If active release complete, move to done queue
        if self.active_q[0].is_done():
            logger.info("Release %s complete, moving to done list", current)
            current.mark_released(new_tick)
            self.done_q.append(self.active_q.popleft())

        self.tick = new_tick
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
