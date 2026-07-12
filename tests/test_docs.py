#!/usr/bin/env python3
"""
Tests for codespace-edge-rd documentation repository integrity.
Run: python3 -m pytest tests/test_docs.py -v
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_readme_exists():
    """README.md must exist."""
    assert (REPO_ROOT / "README.md").exists()


def test_readme_describes_purpose():
    """README must describe Codespace→Edge research."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "Codespace" in content or "codespace" in content
    assert "Edge" in content or "edge" in content


def test_readme_has_yoke_transfer():
    """README must mention yoke transfer concept."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "yoke" in content.lower(), "README should discuss yoke transfer"


def test_readme_has_crystallization():
    """README must reference crystallization."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "crystallization" in content.lower(), "README should discuss crystallization"


def test_readme_has_quick_start():
    """README must have a Quick Start section."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "Quick Start" in content or "quick start" in content.lower()


def test_license_is_mit():
    """LICENSE must be MIT."""
    content = (REPO_ROOT / "LICENSE").read_text()
    assert "MIT License" in content


def test_charter_exists():
    """CHARTER.md must exist."""
    assert (REPO_ROOT / "CHARTER.md").exists()


def test_charter_has_mission():
    """CHARTER must state a mission."""
    content = (REPO_ROOT / "CHARTER.md").read_text()
    assert "Mission" in content or "mission" in content.lower()


def test_docs_directory():
    """docs/ directory should exist with documentation."""
    docs = REPO_ROOT / "docs"
    assert docs.exists(), "docs/ directory must exist"
    assert docs.is_dir()
    md_files = list(docs.glob("*.md"))
    assert len(md_files) >= 2, f"Expected 2+ docs, found {len(md_files)}"


def test_future_integration_doc():
    """docs/FUTURE-INTEGRATION.md should exist and have substance."""
    f = REPO_ROOT / "docs" / "FUTURE-INTEGRATION.md"
    if f.exists():
        content = f.read_text()
        assert len(content) > 200, "FUTURE-INTEGRATION.md should be substantial"


def test_gitignore_exists():
    """.gitignore must exist."""
    assert (REPO_ROOT / ".gitignore").exists()


def test_gitignore_covers_artifacts():
    """.gitignore should cover build artifacts and dependencies."""
    content = (REPO_ROOT / ".gitignore").read_text()
    assert "target/" in content or "__pycache__" in content or "node_modules" in content


def test_devcontainer_docs():
    """README should mention devcontainer templates."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "devcontainer" in content.lower(), "README should discuss devcontainer templates"


def test_edge_targets_documented():
    """README should document edge target hardware."""
    content = (REPO_ROOT / "README.md").read_text()
    has_jetson = "jetson" in content.lower()
    has_pi = "pi" in content.lower() or "raspberry" in content.lower()
    assert has_jetson or has_pi, "README should mention edge hardware targets"


def test_bandwidth_budget_documented():
    """README should include bandwidth budget information."""
    content = (REPO_ROOT / "README.md").read_text()
    assert "bandwidth" in content.lower() or "Mbps" in content, "Should document bandwidth constraints"
