#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 9.
"""

from Chapter_16.ch16_ex9 import Log_Producer, Log_Consumer_1
import logging
import logging.handlers
import yaml
import queue

# Modified Queue Handler
# ==================================

# Extended QueueHandler class


class WaitQueueHandler(logging.handlers.QueueHandler):

    def enqueue(self, record):
        self.queue.put(record)


# Revised Producer


class Log_Producer_2(Log_Producer):
    handler_class = WaitQueueHandler


# The Queue

import multiprocessing

queue2: multiprocessing.Queue = multiprocessing.Queue(100)  # Waaayyyy too small

# The consumer process

consumer2 = Log_Consumer_1(queue2)
consumer2.start()

# The producers

producers = []
for i in range(10):
    proc = Log_Producer_2(i, queue2)
    proc.start()
    producers.append(proc)

# Normal termination

for p in producers:
    p.join()

queue2.put(None)

consumer2.join()

logging.shutdown()

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
