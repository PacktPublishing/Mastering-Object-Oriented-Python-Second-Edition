#!/usr/bin/env python3
"""Run all the chapter modules, doctests or performance() function

This is run from the top-level directory, where all of the sample
data files are also located.

When runnning individual examples, working directory is expected
to be this top-level directory.
"""
import doctest
import runpy
import unittest
import sys
import time
from enum import Enum
import importlib
from pathlib import Path
from typing import Any, Iterator, Tuple, Iterable
import pytest

DEBUG = False # Can't easily use logging -- can conflict with chapters on logging.

DOCTEST_EXCLUDE = {
    'ch13_ex4'  # Requires a separate server to be started, too complex for this script
}

def package_module_iter(packages: Iterable[Path]) -> Iterator[Tuple[Path, Iterator[Path]]]:
    """For a given list of packages, emit the package name and a generator
    for all modules in the package. Structured like ``itertools.groupby()``.
    With a filter to reject caches of various kinds.

    keep = lambda path: not all(
        [filename.stem.startswith("__"), filename.stem.endswith("__"), filename.suffix == ".py"]
    )
    yield package, filter(keep, package.glob("*.py"))
    """
    def module_iter(package: Path, module_iter: Iterable[Path]) -> Iterator[Path]:
        """
        A filter to reject __init__.py and similar names.
        """
        if DEBUG:
            print(f"Package {package}")
        for filename in module_iter:
            if (
                filename.stem.startswith("__")
                and filename.stem.endswith("__")
                and filename.suffix == ".py"
            ):
                continue
            if DEBUG:
                print(f"  file {filename.name} module {filename.stem}")
            yield filename

    for package in packages:
        yield (package,
               module_iter(package, package.glob("*.py")))

def run(pkg_mod_iter: Iterable[Tuple[Path, Iterable[Path]]]) -> None:
    """Run each module, with a few exclusions."""
    for package, module_iter in pkg_mod_iter:
        print()
        print(package.name)
        print("="*len(package.name))
        print()
        for module in module_iter:
            if module.stem in DOCTEST_EXCLUDE:
                print(f"Excluding {module}")
                continue
            status = runpy.run_path(module, run_name="__main__")
            if status != 0:
                sys.exit(f"Failure: {module}")
import subprocess

def run_doctest_suite(pkg_mod_iter: Iterable[Tuple[Path, Iterable[Path]]]) -> None:
    """Doctest each module individually. With a few exclusions.

    Might be simpler to use doctest.testfile()? However, the examples aren't laid out for this.
    """
    for package, module_iter in pkg_mod_iter:
        print()
        print(package.name)
        print("="*len(package.name))
        print()
        for module_path in module_iter:
            if module_path.stem in DOCTEST_EXCLUDE:
                print(f"Excluding {module_path}")
                continue
            result = subprocess.run(['python3', '-m', 'doctest', str(module_path)])
            if result.returncode != 0:
                sys.exit(f"Failure {result!r} in {module_path}")

class PytestExit(int, Enum):
    Success = 0
    Failures = 1
    Interrupted = 2
    InternalError = 3
    CommandLineError = 4
    NoTests = 5

def run_pytest_suite(pkg_mod_iter: Iterable[Tuple[Path, Iterable[Path]]]) -> None:
    """Pytest each module's modules.
    """
    for package, module_iter in pkg_mod_iter:
        print()
        print(package.name)
        print("="*len(package.name))
        print()
        names = [f"{m.parent.name}/{m.name}" for m in (module_iter)]
        print(names)
        status = pytest.main(names)
        if status not in (PytestExit.Success, PytestExit.NoTests):
            sys.exit(f"Failure {PytestExit(status)!r} in {names}")


def run_performance(pkg_mod_iter: Iterable[Tuple[Path, Iterable[Path]]]) -> None:
    """Locate a performance() function in each module and run it."""
    for package, module_iter in pkg_mod_iter:
        print()
        print(package.name)
        print("="*len(package.name))
        print()
        for module in module_iter:
            print(module)
            try:
                imported_module = __import__(
                    f"{package.name}.{module.stem}", fromlist=[module.stem, "performance"])
                imported_module.performance()
            except AttributeError:
                pass # no performance() function in the module.

def master_test_suite(pkg_mod_iter: Iterable[Tuple[Path, Iterable[Path]]]) -> None:
    """Deprecated. Use pytest, instead.

    Build a master unittest test suite from all modules and run that.
    """
    master_suite = unittest.TestSuite()
    for package, module_iter in pkg_mod_iter:
        for module in module_iter:
            print(f"{package.name}.{module.stem}", file=sys.stderr)
            suite = doctest.DocTestSuite(f"{package.name}.{module.stem}")
            print("  ", suite, file=sys.stderr)
            master_suite.addTests(suite)
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(master_suite)

def chap_key(name: Path) -> int:
    _, _, n = name.stem.partition("_")
    return int(n)

if __name__ == "__main__":
    content = sorted(Path.cwd().glob("Chapter_*"), key=chap_key)
    if DEBUG:
        print(content, file=sys.stderr)
    run_doctest_suite(package_module_iter(content))
    run_pytest_suite(package_module_iter(content))
