"""Tests of the schemas, the loader and the resolution of the configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

from horai.io.config import ConfigurationError, resolve_configuration
from horai.io.loader import load_plan
from horai.io.schemas import SchemaSet


def test_every_record_type_has_a_schema(schemas: SchemaSet) -> None:
    expected = {
        "configuration",
        "profile",
        "availability",
        "purpose",
        "deliverable",
        "milestone",
        "question",
        "standing",
        "week-template",
        "cycle",
        "week",
        "appointment",
        "inbox",
        "holding",
        "ideas",
        "archive",
        "clock-log",
        "decision-log",
        "deviation-log",
    }
    assert set(schemas.types()) == {f"horai:{name}@1" for name in expected}


def test_fixture_loads_without_issue(plan_folder: Path, schemas: SchemaSet) -> None:
    plan, issues = load_plan(plan_folder, schemas)
    assert issues == []
    assert set(plan.items) == {
        "ctx-population-fit",
        "ctx-rank-bound",
        "gating-under-noise",
        "mathematics-floor",
    }
    assert plan.items["gating-under-noise"].kind == "question"
    assert len(plan.clock) == 5


def test_invalid_file_is_reported_and_excluded(plan_folder: Path, schemas: SchemaSet) -> None:
    path = plan_folder / "plan" / "milestones" / "ctx-rank-bound.yml"
    path.write_text(path.read_text().replace("budget: PT6H", "budget: 6h"))
    plan, issues = load_plan(plan_folder, schemas)
    assert [issue.rule for issue in issues] == ["schema/invalid"]
    assert "6h" in issues[0].message and issues[0].path == "plan/milestones/ctx-rank-bound.yml"
    assert "ctx-rank-bound" not in plan.items and "ctx-rank-bound" in plan.excluded


@pytest.mark.parametrize(
    ("relative", "old", "new", "rule"),
    [
        (
            "plan/questions/gating-under-noise.yml",
            "horai:question@1",
            "horai:milestone@1",
            "schema/type",
        ),
        (
            "calendar/weeks/2026-11-09.yml",
            "opened: 2026-11-09",
            "opened: 2026-11-10",
            "identifier/week",
        ),
        ("log/clock/2026-11.yml", "month: 2026-11", "month: 2026-10", "identifier/month"),
        ("plan/standing/mathematics-floor.yml", "title:", "title: [", "file/unreadable"),
    ],
)
def test_file_defects_are_reported(
    plan_folder: Path, schemas: SchemaSet, relative: str, old: str, new: str, rule: str
) -> None:
    path = plan_folder / relative
    path.write_text(path.read_text().replace(old, new, 1))
    _, issues = load_plan(plan_folder, schemas)
    assert rule in {issue.rule for issue in issues}


def test_file_name_must_be_a_slug(plan_folder: Path, schemas: SchemaSet) -> None:
    folder = plan_folder / "plan" / "purposes"
    (folder / "thesis.yml").rename(folder / "My_Thesis.yml")
    _, issues = load_plan(plan_folder, schemas)
    assert "identifier/form" in {issue.rule for issue in issues}


def test_configuration_defaults_to_the_current_folder(plan_folder: Path) -> None:
    configuration = resolve_configuration(None, None, {}, plan_folder)
    assert configuration.plan == plan_folder.resolve() and configuration.path is None


def test_configuration_file_found_from_a_subfolder(plan_folder: Path) -> None:
    (plan_folder / "horai.yml").write_text(
        "_schema: horai:configuration@1\ntimezone: Europe/Paris\n"
    )
    configuration = resolve_configuration(None, None, {}, plan_folder / "plan" / "milestones")
    assert (
        configuration.root == plan_folder.resolve()
        and str(configuration.timezone) == "Europe/Paris"
    )


def test_two_configuration_files_compete(plan_folder: Path) -> None:
    (plan_folder / "horai.yml").write_text("_schema: horai:configuration@1\n")
    (plan_folder / "config" / "tools").mkdir(parents=True)
    (plan_folder / "config" / "tools" / "horai.yml").write_text("_schema: horai:configuration@1\n")
    with pytest.raises(ConfigurationError, match="compete"):
        resolve_configuration(None, None, {}, plan_folder)


def test_configuration_at_an_arbitrary_path(plan_folder: Path, tmp_path: Path) -> None:
    custom = tmp_path / "elsewhere" / "settings.yml"
    custom.parent.mkdir()
    custom.write_text(f"_schema: horai:configuration@1\nplan: {plan_folder}\n")
    by_option = resolve_configuration(None, custom, {}, tmp_path)
    by_variable = resolve_configuration(None, None, {"HORAI_CONFIG": str(custom)}, tmp_path)
    assert by_option.plan == by_variable.plan == plan_folder.resolve()


@pytest.mark.parametrize(
    "content",
    [
        "_schema: other:configuration@1\n",
        "_schema: horai:configuration@1\nbogus: 1\n",
        "_schema: horai:configuration@1\ntimezone: Mars/Olympus\n",
    ],
)
def test_invalid_configuration_is_an_error(plan_folder: Path, content: str) -> None:
    (plan_folder / "horai.yml").write_text(content)
    with pytest.raises(ConfigurationError):
        resolve_configuration(None, None, {}, plan_folder)


def test_named_configuration_must_exist(plan_folder: Path) -> None:
    with pytest.raises(ConfigurationError, match="not found"):
        resolve_configuration(None, plan_folder / "absent.yml", {}, plan_folder)


def test_stream_identifier_must_be_a_slug(plan_folder: Path, schemas: SchemaSet) -> None:
    path = plan_folder / "profile.yml"
    path.write_text(path.read_text().replace("{id: tools,", "{id: T,"))
    _, issues = load_plan(plan_folder, schemas)
    assert [issue.rule for issue in issues] == ["schema/invalid"]
    assert "streams/1/id: 'T' is not a slug" in issues[0].message
