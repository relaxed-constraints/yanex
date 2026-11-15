"""Verify shared API settings and release/manual publishing."""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_inherited_api_defaults():
    config_module = pytest.importorskip("zensical.config")
    config = config_module.parse_config(str(ROOT / "mkdocs.yml"))
    handler = config["plugins"]["mkdocstrings"]["config"]["handlers"]["python"]
    assert handler["paths"] == ["."]
    assert handler["options"]["members_order"] == "alphabetical"
    assert handler["options"]["filters"] == ["!^_"]
    assert handler["options"]["show_source"] is False
    sections = config["plugins"]["llmstxt"]["config"]["sections"]
    assert "CLI reference" in [section["title"] for section in sections]
    assert "API reference" in [section["title"] for section in sections]


def test_pages_publishes_only_releases_or_manual_dispatch():
    workflow = yaml.load(
        (ROOT / ".github/workflows/pages.yml").read_text(), Loader=yaml.BaseLoader
    )
    assert workflow["on"] == {
        "workflow_dispatch": "",
        "release": {"types": ["published"]},
    }
    assert (
        "relcon-docs/.github/workflows/deploy-docs.yml@"
        in workflow["jobs"]["docs"]["uses"]
    )
