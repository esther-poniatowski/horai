"""
Reading of YAML with the scalar types of the YAML 1.2 core schema.

PyYAML follows YAML 1.1, which reads ``2026-11-13`` as a date, ``10:00`` as the integer 600 and
``no`` as false. The records of a plan hold dates, hours and durations as strings, which their
schemas validate, so this loader keeps such scalars as strings. It resolves only ``true`` and
``false`` as booleans, and only decimal numbers as integers and floats.

Functions
---------
load_yaml(text) -> Any
    Parse a YAML document with the scalar types of the YAML 1.2 core schema.
"""

from __future__ import annotations

import re
from typing import Any

import yaml


class CoreLoader(yaml.SafeLoader):  # pylint: disable=too-many-ancestors
    """A safe loader that resolves the scalar types of the YAML 1.2 core schema only."""


CoreLoader.yaml_implicit_resolvers = {}
for _tag, _pattern, _first in [
    ("tag:yaml.org,2002:bool", r"^(?:true|True|TRUE|false|False|FALSE)$", "tTfF"),
    ("tag:yaml.org,2002:int", r"^[-+]?[0-9]+$", "-+0123456789"),
    (
        "tag:yaml.org,2002:float",
        r"^[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?$",
        "-+.0123456789",
    ),
    ("tag:yaml.org,2002:null", r"^(?:~|null|Null|NULL|)$", "~nN"),
]:
    # The resolver of an empty scalar is registered under the empty string.
    _starts = list(_first) + ([""] if _tag.endswith(":null") else [])
    CoreLoader.add_implicit_resolver(_tag, re.compile(_pattern), _starts)


def load_yaml(text: str) -> Any:
    """Parse a YAML document with the scalar types of the YAML 1.2 core schema.

    Examples
    --------
    >>> load_yaml("day: 2026-11-13\\nstart: 10:00\\nanswer: no\\nrisk: true")
    {'day': '2026-11-13', 'start': '10:00', 'answer': 'no', 'risk': True}
    """
    return yaml.load(text, Loader=CoreLoader)  # noqa: S506 - CoreLoader derives from SafeLoader
