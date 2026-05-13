"""
Feature-level conftest to enable direct .feature execution by loading
the shared pytest fixtures and step definitions from the test layer.
"""

from importlib import import_module
from pkgutil import iter_modules

from src.tests import step_defs as step_defs_pkg

pytest_plugins = ["src.tests.conftest"]


def is_step_definition_module(module_name: str) -> bool:
    module_basename = module_name.rsplit(".", 1)[-1]
    return module_basename.startswith("test_") and module_basename.endswith("_steps")


for module in iter_modules(step_defs_pkg.__path__, f"{step_defs_pkg.__name__}."):
    if not is_step_definition_module(module.name):
        continue
    import_module(module.name)
