from __future__ import annotations

from dataclasses import dataclass

import argparse
import subprocess
import sys
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    browser_name: str = "chromium"
    headless: bool = True


class TestRunner:
    """Utility class to run pytest with different configurations"""

    def __init__(self):
        self.test_dir = Path(__file__).parents[2] / "src" / "tests"

    def run_all_tests(self, verbose=True):
        cmd = ["python", "-m", "pytest"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_smoke_tests(self, verbose=True):
        cmd = ["python", "-m", "pytest", "-m", "smoke"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_regression_tests(self, verbose=True):
        cmd = ["python", "-m", "pytest", "-m", "regression"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_critical_tests(self, verbose=True):
        cmd = ["python", "-m", "pytest", "-m", "critical"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_specific_test_class(self, class_name, verbose=True):
        cmd = ["python", "-m", "pytest", f"test_business_functions.py::{class_name}"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_specific_test(self, class_name, test_name, verbose=True):
        cmd = ["python", "-m", "pytest", f"test_business_functions.py::{class_name}::{test_name}"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_with_coverage(self, verbose=True):
        cmd = ["python", "-m", "pytest", "--cov=src", "--cov-report=html"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_with_html_report(self, verbose=True):
        cmd = ["python", "-m", "pytest", "--html=reports/report.html", "--self-contained-html"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_in_parallel(self, verbose=True):
        cmd = ["python", "-m", "pytest", "-n", "auto"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)

    def run_with_timeout(self, timeout=300, verbose=True):
        cmd = ["python", "-m", "pytest", f"--timeout={timeout}"]
        if verbose:
            cmd.append("-v")
        subprocess.run(cmd, cwd=self.test_dir)


def main():
    parser = argparse.ArgumentParser(description="Test Runner for Automation Framework")
    parser.add_argument(
        "--type",
        choices=["all", "smoke", "regression", "critical", "class", "test"],
        default="all",
        help="Type of tests to run",
    )
    parser.add_argument("--class", dest="test_class", help="Specific test class to run (use with --type=class)")
    parser.add_argument("--test", help="Specific test to run (use with --type=test)")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--html", action="store_true", help="Generate HTML test report")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout for tests in seconds")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode (less verbose output)")

    args = parser.parse_args()
    runner = TestRunner()
    verbose = not args.quiet

    try:
        if args.coverage:
            runner.run_with_coverage(verbose=verbose)
        elif args.html:
            runner.run_with_html_report(verbose=verbose)
        elif args.parallel:
            runner.run_in_parallel(verbose=verbose)
        elif args.type == "all":
            runner.run_all_tests(verbose=verbose)
        elif args.type == "smoke":
            runner.run_smoke_tests(verbose=verbose)
        elif args.type == "regression":
            runner.run_regression_tests(verbose=verbose)
        elif args.type == "critical":
            runner.run_critical_tests(verbose=verbose)
        elif args.type == "class":
            if not args.test_class:
                sys.exit(1)
            runner.run_specific_test_class(args.test_class, verbose=verbose)
        elif args.type == "test":
            if not args.test_class or not args.test:
                sys.exit(1)
            runner.run_specific_test(args.test_class, args.test, verbose=verbose)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()

