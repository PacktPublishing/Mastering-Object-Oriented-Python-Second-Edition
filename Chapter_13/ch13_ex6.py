#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 6.
"""

# Multiprocessing Example
# =========================

# We want a Simulation process to cough up some statistics

# Import the simulation model...
from Chapter_13.simulation_model import *

import multiprocessing


class Simulation(multiprocessing.Process):

    def __init__(
        self,
        setup_queue: multiprocessing.SimpleQueue,
        result_queue: multiprocessing.SimpleQueue,
    ) -> None:
        self.setup_queue = setup_queue
        self.result_queue = result_queue
        super().__init__()

    def run(self) -> None:
        """Waits for a termination"""
        print(f"{self.__class__.__name__} start")
        item = self.setup_queue.get()
        while item != (None, None):
            table, player = item
            self.sim = Simulate(table, player, samples=1)
            results = list(self.sim)
            self.result_queue.put((table, player, results[0]))
            item = self.setup_queue.get()
        print(f"{self.__class__.__name__} finish")


# We want a Summarization process to gather and summarize all those stats.
class Summarize(multiprocessing.Process):

    def __init__(self, queue: multiprocessing.SimpleQueue) -> None:
        self.queue = queue
        super().__init__()

    def run(self) -> None:
        """Waits for a termination"""
        print(f"{self.__class__.__name__} start")
        count = 0
        item = self.queue.get()
        while item != (None, None, None):
            print(item)
            count += 1
            item = self.queue.get()
        print(f"{self.__class__.__name__} finish {count}")


# Create and run the simulation
# -----------------------------


def server_6() -> None:

    # Two queues
    setup_q: multiprocessing.SimpleQueue = multiprocessing.SimpleQueue()
    results_q: multiprocessing.SimpleQueue = multiprocessing.SimpleQueue()

    # The summarization process: waiting for work
    result = Summarize(results_q)
    result.start()

    # The simulation process: also waiting for work.
    # We might want to create a Pool of these so that
    # we can get even more done at one time.
    simulators = []
    for i in range(4):
        sim = Simulation(setup_q, results_q)
        sim.start()
        simulators.append(sim)

    # Queue up some objects to work on.
    table = Table(decks=6, limit=50, dealer=Hit17(), split=ReSplit(), payout=(3, 2))
    for bet in Flat, Martingale, OneThreeTwoSix:
        player = Player(SomeStrategy(), bet(), 100, 25)
        for sample in range(5):
            setup_q.put((table, player))

    # Queue a terminator for each simulator.
    for sim in simulators:
        setup_q.put((None, None))

    # Wait for the simulations to all finish.
    for sim in simulators:
        sim.join()

    # Queue up a results terminator.
    # Results processing done?
    results_q.put((None, None, None))
    result.join()
    del results_q
    del setup_q


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    server_6()
