"""
The JSON Schemas of the records, shipped as package data.

Each record type has one schema file in ``horai/data/schemas``, and the definitions shared by
several types live in ``common.schema.yml``. The schemas are the contract of the record formats:
horai validates every file against them, and Ekphrasis builds its forms from them.

Classes
-------
SchemaSet
    The validators of every record type, keyed by the value of `_schema`.
"""

from __future__ import annotations

from collections.abc import Iterator
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT202012

from .yaml_loader import load_yaml


class SchemaSet:
    """The validators of every record type, keyed by the value of `_schema`.

    Examples
    --------
    >>> schemas = SchemaSet.load()
    >>> "horai:milestone@1" in schemas.types()
    True
    """

    def __init__(self, documents: dict[str, dict[str, Any]]) -> None:
        resources = [(doc["$id"], DRAFT202012.create_resource(doc)) for doc in documents.values()]
        registry: Registry = Registry().with_resources(resources)
        self._validators: dict[str, Draft202012Validator] = {}
        for name, document in documents.items():
            if name == "common":
                continue
            constant = document["properties"]["_schema"]["const"]
            self._validators[constant] = Draft202012Validator(
                document, registry=registry, format_checker=FormatChecker()
            )

    @classmethod
    def load(cls) -> SchemaSet:
        """Load the schema files shipped with the package."""
        documents = {}
        for entry in files("horai").joinpath("data", "schemas").iterdir():
            if entry.name.endswith(".schema.yml"):
                documents[entry.name.removesuffix(".schema.yml")] = load_yaml(
                    entry.read_text(encoding="utf-8")
                )
        return cls(documents)

    def types(self) -> list[str]:
        """Return the identifiers of the record types, such as ``horai:milestone@1``."""
        return sorted(self._validators)

    def errors(self, schema_id: str, data: Any) -> Iterator[str]:
        """Yield one message per violation of the schema `schema_id` by `data`.

        Each message starts with the path of the value at fault, such as ``tasks/0/budget``.
        """
        validator = self._validators[schema_id]
        for error in sorted(
            validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path))
        ):
            location = "/".join(str(part) for part in error.absolute_path) or "(root)"
            description = (
                error.schema.get("description") if isinstance(error.schema, dict) else None
            )
            if error.validator in ("pattern", "format") and description:
                yield f"{location}: {error.instance!r} is not {description}"
            else:
                yield f"{location}: {error.message}"
