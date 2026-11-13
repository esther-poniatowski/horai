"""Pytest configuration and shared fixtures for horai tests."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pytest

from horai.domain.records import Plan
from horai.io.loader import load_plan
from horai.io.schemas import SchemaSet

FIXTURE_PLAN = Path(__file__).parent / "fixtures" / "plans" / "research"
DAY = date(2026, 11, 13)


@pytest.fixture(scope="session")
def schemas() -> SchemaSet:
    """The schemas shipped with the package."""
    return SchemaSet.load()


@pytest.fixture
def plan_folder(tmp_path: Path) -> Path:
    """A copy of the research fixture plan, which a test may modify."""
    target = tmp_path / "plan"
    shutil.copytree(FIXTURE_PLAN, target)
    return target


@pytest.fixture
def plan(schemas: SchemaSet) -> Plan:
    """The records of the research fixture plan, which loads without issue."""
    loaded, issues = load_plan(FIXTURE_PLAN, schemas)
    assert issues == []
    return loaded
