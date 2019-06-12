#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 4.
"""


# Startup/Shutdown
# =============================================

# Some main function

from typing import Dict, Counter
import logging

import collections
from Chapter_16.ch16_ex1 import LoggedClass


class Main(LoggedClass):

    def __init__(self) -> None:
        self.counts: Counter[str] = collections.Counter()

    def run(self) -> int:
        self.logger.info("Start")

        # Some processing in and around the counter increments
        self.counts["input"] += 2000
        self.counts["reject"] += 500
        self.counts["output"] += 1500

        self.logger.info("Counts %s", self.counts)

        for k in self.counts:
            self.logger.info(f"{k:.<16s} {self.counts[k]:>6,d}")

        return 0


config3 = """
version: 1
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: control
  audit_file:
    class: logging.FileHandler
    filename: data/ch16_audit.log
    encoding: utf-8
    formatter: basic
formatters:
  control:
    style: "{"
    format: "{levelname:s}:{message:s}"
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
loggers:
  verbose:
    handlers: [console]
    level: INFO
    propagate: False # Added
  audit:
    handlers: [console,audit_file]
    level: INFO
    propagate: False # Added
root: # Added
  handlers: [console]
  level: INFO
disable_existing_loggers: False
"""

# Main program


def demo4a() -> None:
    import sys
    import logging
    import logging.config
    import yaml

    logging.config.dictConfig(yaml.load(config3))
    try:
        application = Main()
        status = application.run()
    except Exception as e:
        logging.exception(e)
        status = 2
    finally:
        logging.shutdown()
    # sys.exit(status)


# Atexit


def demo4b() -> None:
    import atexit
    import logging
    import logging.config
    import yaml
    import sys

    logging.config.dictConfig(yaml.load(config3))
    atexit.register(logging.shutdown)
    try:
        application = Main()
        status = application.run()
    except Exception as e:
        logging.exception(e)
        status = 2
    # sys.exit(status)


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    demo4a()
    demo4b()
