"""
BDD Test Driver - Feature file scenarios converted to pytest-bdd tests
Imports and registers all step definitions before generating tests from feature file.
"""

from __future__ import annotations

from pathlib import Path

# Import step definitions FIRST - must be before scenarios() call
from src.tests.step_defs import test_saucedemo_steps  # noqa: F401

from pytest_bdd import scenarios

# Load feature file scenarios
FEATURE_FILE = Path(__file__).resolve().parents[2] / "features" / "web" / "login_to_cart.feature"

# Load all scenarios from feature file
scenarios(str(FEATURE_FILE))


