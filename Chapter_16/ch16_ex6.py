#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 6.
"""

from typing import Optional
import logging
import logging.config
import yaml
import getpass


config5 = """
version: 1
disable_existing_loggers: False
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: basic
  audit_file:
    class: logging.FileHandler
    filename: data/ch16_audit.log
    encoding: utf-8
    formatter: detailed
formatters:
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
  detailed:
    style: "{"
    format: "{levelname:s}:{name:s}:{asctime:s}:{message:s}"
    datefmt: "%Y-%m-%d %H:%M:%S"
loggers:
  audit:
    handlers: [console,audit_file]
    level: INFO
    propagate: False
root:
  handlers: [console]
  level: INFO
"""

# Extending
# ====================

# Doesn't seem to work as expected.

# Note that the factory is somehow bypassed by a LoggerAdapter
# Also. Thus mystifies mypy because we're adding attributes to the base class.

class UserLogRecordFactory:
    def __init__(self) -> None:
        self.user: Optional[str] = None
        self.previous = logging.getLogRecordFactory()

    def __call__(self, *args, **kwargs) -> logging.LogRecord:
        print("Building log with ", args, kwargs)
        user = getpass.getuser()
        record = self.previous(*args, **kwargs)
        record.user = user  # type: ignore
        return record

# Adapter. This kind of extension may not be needed.
# The "extra" is set as the default behavior.
# However, the processing is obscure. It behaves as if it bypassed the factory.
# Yet. The code looks like it won't bypass the factory.

class UserLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs['user'] = self.extra.get('user', None)
        return msg, kwargs

# Installation

logging.config.dictConfig(yaml.load(config5))
logging.setLogRecordFactory(UserLogRecordFactory())

# Use

log = logging.getLogger("test.demo6")
for h in logging.getLogger().handlers:
    h.setFormatter(logging.Formatter(fmt="{user}:{name}:{levelname}:{message}", style="{"))

import threading
data = threading.local()
data.user = "Some User"
data.ip_address = "127.0.0.1"

log.info("message without User")
log.info("message with user")
log.info("message with extra", extra={"more": "More Data"})

# auth_log = logging.LoggerAdapter( log, data.__dict__ )  # "Attempt to overwrite 'user' in LogRecord"
# auth_log = UserLogAdapter( log, data.__dict__ )  # _log() got an unexpected keyword argument 'user'
# auth_log.info( "message with User" )


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
