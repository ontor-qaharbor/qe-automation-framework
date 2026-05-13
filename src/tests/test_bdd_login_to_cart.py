"""
BDD Test Driver - Feature file scenarios converted to pytest-bdd tests
"""
import pytest
from pathlib import Path
from pytest_bdd import scenarios

# Import step definitions to make them available to the scenarios
# Moving this to the top helps IDEs like PyCharm resolve steps in feature files
from steps.test_saucedemo_steps import *

# Load feature file path
FEATURE_FILE = Path(__file__).resolve().parents[2] / "features" / "web" / "login_to_cart.feature"

# Automatically create tests for all scenarios in the feature file
scenarios(FEATURE_FILE)
