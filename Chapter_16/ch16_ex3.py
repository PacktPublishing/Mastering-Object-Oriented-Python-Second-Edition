#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 3.
"""


# Multiple Loggers with YAML Config
# =============================================

# Sample configuration file

config3 = """
version: 1
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: basic
  audit_file:
    class: logging.FileHandler
    filename: data/ch16_audit.log
    encoding: utf-8
    formatter: basic
formatters:
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
"""


import logging.config
import yaml

config_dict = yaml.load(config3)
print(config_dict)

logging.config.dictConfig(config_dict)

# Logging

verbose = logging.getLogger("verbose.example.SomeClass")
audit = logging.getLogger("audit.example.SomeClass")
verbose.info("Verbose information")
audit.info("Audit record with before and after")

print("Root Handlers:", logging.getLogger().handlers)
print("Verbose Handlers:", logging.getLogger('verbose').handlers)
print("Audit Handlers:", logging.getLogger('audit').handlers)


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
