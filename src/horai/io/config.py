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
    roots : tuple[Path, ...]
        Folders under which the records of the hierarchy are found by their key `_schema`.
    exclude : tuple[str, ...]
        Patterns of paths, relative to a root, under which no record is sought.
    """

    root: Path
    plan: Path
    timezone: ZoneInfo | None
    path: Path | None
    roots: tuple[Path, ...] = ()
    exclude: tuple[str, ...] = ()


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


def _config_path(
    config: Path | None, environ: Mapping[str, str], cwd: Path, root: Path
) -> Path | None:
    """Return the configuration file named by the option or the variable, or found at the root."""
    named = config
    if named is None and environ.get(CONFIG_VARIABLE):
        named = Path(environ[CONFIG_VARIABLE])
    if named is not None:
        path = (named if named.is_absolute() else cwd / named).resolve()
        if not path.is_file():
            raise ConfigurationError(f"configuration file not found: {path}")
        return path
    found = _candidates(root)
    if len(found) > 1:
        raise ConfigurationError(f"two configuration files compete: {found[0]} and {found[1]}")
    return found[0] if found else None


def _read_config(path: Path | None) -> dict[str, Any]:
    """Read and validate the configuration file; without one, the built-in defaults apply."""
    if path is None:
        return {}
    data = load_yaml(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or data.get("_schema") != CONFIG_SCHEMA:
        raise ConfigurationError(f"{path}: the key _schema must hold {CONFIG_SCHEMA}")
    problems = list(SchemaSet.load().errors(CONFIG_SCHEMA, data))
    if problems:
        raise ConfigurationError(f"{path}: " + "; ".join(problems))
    return data


def _timezone(data: dict[str, Any]) -> ZoneInfo | None:
    """Return the configured time zone, or None for the local zone."""
    if "timezone" not in data:
        return None
    zone = data["timezone"]
    try:
        return ZoneInfo(zone)
    except ZoneInfoNotFoundError as error:
        raise ConfigurationError(f"unknown time zone: {zone}") from error


def _folder(path: Path, what: str) -> Path:
    """Return `path` resolved, or raise when it is not a folder."""
    resolved = path.resolve()
    if not resolved.is_dir():
        raise ConfigurationError(f"{what} not found: {resolved}")
    return resolved


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
    path = _config_path(config, environ, cwd, resolved_root)
    data = _read_config(path)
    return Configuration(
        root=resolved_root,
        plan=_folder(resolved_root / data.get("plan", "."), "folder of the plan"),
        timezone=_timezone(data),
        path=path,
        roots=tuple(
            _folder(resolved_root / entry, "root of the plan") for entry in data.get("roots", ())
        ),
        exclude=tuple(data.get("exclude", ())),
    )
