"""
Resolution of the root, the configuration file and the folder of a plan.

The root and the configuration file are found as the conventions of the command line state, with
one extension: the environment variable ``HORAI_CONFIG`` names a configuration file at any path, so
that a path chosen once serves every command, and the plugin sets it from its settings.

Classes
-------
ConfigurationError
    A wrong command line or configuration, reported with the exit status 2.
Configuration
    The resolved configuration of one run.

Functions
---------
resolve_configuration(root, config, environ, cwd) -> Configuration
    Resolve the root, the configuration file and the folder of the plan.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .schemas import SchemaSet
from .yaml_loader import load_yaml

CONFIG_NAME = "horai.yml"
CONFIG_SCHEMA = "horai:configuration@1"
ROOT_VARIABLE = "HORAI_ROOT"
CONFIG_VARIABLE = "HORAI_CONFIG"


class ConfigurationError(Exception):
    """A wrong command line or configuration, reported with the exit status 2."""


@dataclass(frozen=True)
class Configuration:
    """The resolved configuration of one run.

    Attributes
    ----------
    root : Path
        Folder from which the paths of the configuration are resolved.
    plan : Path
        Folder of the plan.
    timezone : ZoneInfo | None
        Time zone of the agent, or None for the local zone of the machine.
    path : Path | None
        Configuration file read, or None when the built-in defaults apply.
    """

    root: Path
    plan: Path
    timezone: ZoneInfo | None
    path: Path | None


def _candidates(folder: Path) -> list[Path]:
    """Return the configuration files present in `folder`, in config/tools/ or at its level."""
    return [
        p for p in (folder / "config" / "tools" / CONFIG_NAME, folder / CONFIG_NAME) if p.is_file()
    ]


def _find_root(cwd: Path) -> Path:
    """Return the nearest ancestor of `cwd` that holds a configuration file, or `cwd`."""
    for folder in (cwd, *cwd.parents):
        if _candidates(folder):
            return folder
    return cwd


def resolve_configuration(
    root: Path | None,
    config: Path | None,
    environ: Mapping[str, str],
    cwd: Path,
) -> Configuration:
    """Resolve the root, the configuration file and the folder of the plan.

    Parameters
    ----------
    root : Path | None
        Value of the option ``--root``.
    config : Path | None
        Value of the option ``--config``.
    environ : Mapping[str, str]
        Environment variables, read for ``HORAI_ROOT`` and ``HORAI_CONFIG``.
    cwd : Path
        Current folder.

    Returns
    -------
    Configuration
        The resolved configuration.

    Raises
    ------
    ConfigurationError
        If a named file is absent, if two configuration files compete, or if the file is invalid.
    """
    if root is None and environ.get(ROOT_VARIABLE):
        root = Path(environ[ROOT_VARIABLE])
    resolved_root = (root if root is not None else _find_root(cwd)).resolve()

    named = (
        config
        if config is not None
        else (Path(environ[CONFIG_VARIABLE]) if environ.get(CONFIG_VARIABLE) else None)
    )
    path: Path | None
    if named is not None:
        path = (named if named.is_absolute() else cwd / named).resolve()
        if not path.is_file():
            raise ConfigurationError(f"configuration file not found: {path}")
    else:
        found = _candidates(resolved_root)
        if len(found) > 1:
            raise ConfigurationError(f"two configuration files compete: {found[0]} and {found[1]}")
        path = found[0] if found else None

    data: dict[str, Any] = {}
    if path is not None:
        data = load_yaml(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict) or data.get("_schema") != CONFIG_SCHEMA:
            raise ConfigurationError(f"{path}: the key _schema must hold {CONFIG_SCHEMA}")
        problems = list(SchemaSet.load().errors(CONFIG_SCHEMA, data))
        if problems:
            raise ConfigurationError(f"{path}: " + "; ".join(problems))

    timezone = None
    if "timezone" in data:
        try:
            timezone = ZoneInfo(data["timezone"])
        except ZoneInfoNotFoundError as error:
            zone = data["timezone"]
            raise ConfigurationError(f"unknown time zone: {zone}") from error
    plan = (resolved_root / data.get("plan", ".")).resolve()
    if not plan.is_dir():
        raise ConfigurationError(f"folder of the plan not found: {plan}")
    return Configuration(root=resolved_root, plan=plan, timezone=timezone, path=path)
