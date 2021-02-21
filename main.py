# This is a sample Python script.
import logging
from copy import deepcopy

from PQScheduler import PQScheduler
from RandomSource import RandomSource
from SQScheduler import SQScheduler
from Simulation import Simulation

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    print("Starting Sim!")

    # Set up two random sources with identical contents
    src = RandomSource()
    src.initialize(10)
    cloned_src = RandomSource()
    cloned_src.initialize_from(deepcopy(src.pool))

    print("Simulating single threaded queue")
    sq = SQScheduler()
    sim = Simulation(source=src, scheduler=sq)
    sim.run()
    sim.output_results()

    print("Simulating single queue with parallel processing")
    pq = PQScheduler()
    sim = Simulation(source=cloned_src, scheduler=pq)
    sim.run()
    sim.output_results()
    print("That's all folks!")


def setup_logging():
    """
    Set up logging: handlers, formatters and loggers
    """
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()
