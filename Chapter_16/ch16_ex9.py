#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 9.
"""

import logging
import logging.config
import logging.handlers
import yaml
import time

# Producer/Consumer
# ==========================

# The Consumer

consumer_config = """
version: 1
disable_existing_loggers: False
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: basic
formatters:
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
loggers:
  combined:
    handlers: [console]
    formatter: detail
    level: INFO
    propagate: False
root:
  handlers: [console]
  level: INFO
"""

import collections
import logging
import multiprocessing


class Log_Consumer_1(multiprocessing.Process):
    """In effect, an instance of QueueListener."""

    def __init__(self, queue):
        self.source = queue
        super().__init__()
        logging.config.dictConfig(yaml.load(consumer_config))
        self.combined = logging.getLogger(f"combined.{self.__class__.__qualname__}")
        self.log = logging.getLogger(self.__class__.__qualname__)
        self.counts = collections.Counter()

    def run(self):
        self.log.info("Consumer Started")
        while True:
            log_record = self.source.get()
            if log_record == None: break
            self.combined.handle(log_record)
            self.counts[log_record.getMessage()] += 1
        self.log.info("Consumer Finished")
        self.log.info(self.counts)


# The Producers

class Log_Producer(multiprocessing.Process):
    handler_class = logging.handlers.QueueHandler

    def __init__(self, proc_id, queue):
        self.proc_id = proc_id
        self.destination = queue
        super().__init__()
        self.log = logging.getLogger(
            f"{self.__class__.__qualname__}.{self.proc_id}")
        self.log.handlers = [self.handler_class(self.destination)]
        self.log.setLevel(logging.INFO)

    def run(self):
        self.log.info(f"Started")
        for i in range(100):
            self.log.info(f"Message {i:d}")
            time.sleep(0.001)
        self.log.info(f"Finished")

def demo():

    # The Queue

    import multiprocessing
    # size = 10  # Too small.
    size = 30  # Better
    queue1: multiprocessing.Queue = multiprocessing.Queue(size)

    # The consumer process

    consumer = Log_Consumer_1(queue1)
    consumer.start()

    # The producers

    producers = []
    for i in range(10):
        proc = Log_Producer(i, queue1)
        proc.start()
        producers.append(proc)

    # Normal termination

    for p in producers:
        p.join()

    queue1.put(None)

    consumer.join()

    logging.shutdown()



__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    demo()
