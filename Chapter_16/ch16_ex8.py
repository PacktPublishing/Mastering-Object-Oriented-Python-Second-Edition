#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 8.
"""


# Tail Buffer
# ========================

# Class Definition

# Note. Logging has no type hints. So. mypy fails here.

import logging
import logging.config
import logging.handlers
import yaml


class TailHandler(logging.handlers.MemoryHandler):
    def shouldFlush(self, record: logging.LogRecord) -> bool:
        """
        Check for buffer full or a record at the flushLevel or higher.
        """
        if record.levelno >= self.flushLevel:
            return True
        while len(self.buffer) > self.capacity:
            self.acquire()
            try:
                del self.buffer[0]
            finally:
                self.release()
        return False

# Configuration

config8 = """
version: 1
disable_existing_loggers: False
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: basic
  tail:
    (): __main__.TailHandler
    target: cfg://handlers.console
    capacity: 5
formatters:
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
loggers:
  test:
    handlers: [tail]
    level: DEBUG
    propagate: False
root:
  handlers: [console]
  level: INFO
"""


# Installation

if __name__ == "__main__":
    logging.config.dictConfig(yaml.load(config8))
    log = logging.getLogger("test.demo8")

    # Use Case 1 -- last 5 before ERROR.

    log.info("Last 5 before error")

    for i in range(20):
        log.debug(f"Message {i:d}")

    log.error("Error causes dump of last 5")

    # Use Case 2 -- last 5 before shutdown.

    log.info("Last 5 before shutdown")

    for i in range(20, 40):
        log.debug(f"Message {i:d}")

    log.info("Shutdown causes dump of last 5")

    logging.shutdown()



__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
