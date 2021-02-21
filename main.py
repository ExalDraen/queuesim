# This is a sample Python script.
import logging

from RandomSource import RandomSource
from SQScheduler import SQScheduler
from Simulation import Simulation

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    print("Starting Sim!")
    src = RandomSource(10)
    sched = SQScheduler()
    sim = Simulation(source=src, scheduler=sched)
    sim.run()
    sim.output_results()
    print("That's all folks!")


def setup_logging():
    """
    Set up logging: handlers, formatters and loggers
    """
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()
