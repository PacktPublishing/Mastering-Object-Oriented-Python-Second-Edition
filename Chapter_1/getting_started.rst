In order to run the examples mentioned in this book you require the following software:

- Python version 3.7 or higher with the standard suite of libraries.

We'll look at some additional packages. These include PyYaml, SQLAlchemy, and Jinja2.
We'll use pytest for doing unit testing.

- http://pyyaml.org

- http://www.sqlalchemy.org When building this, check the installation guide, http://docs.sqlalchemy.org/en/rel_0_9/intro.html#installation. Using the --without-cextensions option can simplify installation.

- http://jinja.pocoo.org/

We'll also look at some tools:

- https://docs.pytest.org/en/latest/index.html

- http://sphinx-doc.org

- http://mypy-lang.org

- https://www.pylint.org

- https://github.com/ambv/black


There two alternative approaches to these installations.

-   From Python.org

    1.  Install Python 3.7 from http://www.python.org. This will change your OS-level ``PATH`` settings.
        This usually means you need to start a new terminal session to make your new Python tools available.

    2.  Use your new pip3 to install the other packages:

		  ``python3 -m pip install pyyaml sqlalchemy jinja2 pytest sphinx mypy pylint black``

    If you install from Python.org, you'll have a single, default Python environment. This isn't optimal.
    When you need to upgrade or experiment, you'll often want to create additional environments. There
    are several tools for this. The conda tool seems to be the most versatile.

-   Use Anaconda.com's miniconda to get started.

    1.  Download and install the appropriate miniconda for your platform. https://conda.io/miniconda.html

    2.  Use miniconda to build a Python environment including the required packages.

        ``conda create --name mastering python=3.7 pyyaml sqlalchemy jinja2 pytest sphinx mypy pylint``

    3.  Activate your new environment

        ``conda activate mastering``

        You'll know it's active because your terminal prompt will have ``(mastering)`` as a prefix.

    4.  Add the ``black`` tool using a separate installation after activating the environment.

        ``python3 -m pip install --upgrade pip``

        ``python3 -m pip install black``

