"""
Entry point for the `horai` package, invoked as a module.

Usage
-----
To launch the command-line interface, execute::

    python -m horai


See Also
--------
horai.cli: Module implementing the application's command-line interface.
"""

from .cli import app

app()
