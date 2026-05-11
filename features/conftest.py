"""
Feature-level conftest to enable direct .feature execution by loading
the shared pytest fixtures and step definitions from the test layer.
"""

pytest_plugins = ["src.tests.conftest", "src.tests.step_defs"]
