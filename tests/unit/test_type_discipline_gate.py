"""Tests for scripts/type_discipline_gate.py.

The gate compares each LIT rule's codebase count against the merge-base count, so
what is pinned here is the identity that keys those base counts and the diff scan
that turns a breach into file:line.
"""

from pathlib import Path
from typing import Final

import type_discipline_gate as gate


def test_editing_the_checker_rekeys_the_base_counts(tmp_path: Path) -> None:
    checker: Final = tmp_path / "check.py"
    checker.write_text("print('v1')\n")
    before: Final = gate.checker_identity(checker).artifact_name("abc123")
    assert gate.checker_identity(checker).artifact_name("abc123") == before
    checker.write_text("print('v2')\n")
    assert gate.checker_identity(checker).artifact_name("abc123") != before


def test_parse_changed_lines_groups_hunks_under_their_own_file() -> None:
    diff: Final = (
        "diff --git a/waypoint/a.py b/waypoint/a.py\n"
        "--- a/waypoint/a.py\n"
        "+++ b/waypoint/a.py\n"
        "@@ -0,0 +3,2 @@\n"
        "+one\n"
        "+two\n"
        "diff --git a/waypoint/b.py b/waypoint/b.py\n"
        "--- a/waypoint/b.py\n"
        "+++ b/waypoint/b.py\n"
        "@@ -0,0 +10 @@\n"
        "+only\n"
    )
    changed: Final = gate.parse_changed_lines(diff)
    assert changed["waypoint/a.py"] == {3, 4}
    assert changed["waypoint/b.py"] == {10}


def test_parse_changed_lines_handles_several_hunks_in_one_file() -> None:
    diff: Final = (
        "+++ b/waypoint/a.py\n"
        "@@ -0,0 +1,2 @@\n"
        "+a\n"
        "@@ -9,0 +20,1 @@\n"
        "+b\n"
    )
    assert gate.parse_changed_lines(diff)["waypoint/a.py"] == {1, 2, 20}


def test_parse_changed_lines_on_an_empty_diff_is_empty() -> None:
    assert gate.parse_changed_lines("") == {}


def test_introduced_keeps_only_violations_on_changed_lines() -> None:
    violations: Final = (
        gate.Violation("waypoint/a.py", 3, "LIT006"),
        gate.Violation("waypoint/a.py", 99, "LIT006"),
        gate.Violation("waypoint/b.py", 3, "LIT001"),
    )
    kept: Final = gate.introduced(violations, {"waypoint/a.py": {3}})
    assert kept == [gate.Violation("waypoint/a.py", 3, "LIT006")]


def test_legacy_and_canonical_source_trees_measure_the_same_violations(tmp_path: Path) -> None:
    canonical_root: Final = tmp_path / "current"
    legacy_root: Final = tmp_path / "base"
    for root, name in ((canonical_root, "waypoint"), (legacy_root, "litellm")):
        package: Final = root / name
        package.mkdir(parents=True)
        (package / "probe.py").write_text("def probe():\n    values = []\n    return values\n")
    canonical: Final = gate.count_by_rule(gate._check(canonical_root, gate.CHECKER))
    legacy: Final = gate.count_by_rule(gate._check(legacy_root, gate.CHECKER))
    assert canonical
    assert legacy == canonical
