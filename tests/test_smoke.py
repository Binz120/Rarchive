"""Smoke tests: the package imports and the CLI fails cleanly without credentials."""

import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    """Run ``python -m src`` from the repository root."""
    return subprocess.run(
        [sys.executable, "-m", "src", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class CliSmokeTest(unittest.TestCase):
    """The CLI must work without network access or credentials."""

    def test_help_exits_zero(self) -> None:
        """--help prints usage and exits 0."""
        proc = run_cli("--help")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Archive Reddit posts", proc.stdout)

    def test_missing_credentials_are_reported(self) -> None:
        """Without credentials the CLI exits 1 with a configuration error."""
        env = {k: v for k, v in os.environ.items() if not k.startswith("REDDIT_")}
        proc = run_cli("python", env=env)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("Configuration error", proc.stdout)


if __name__ == "__main__":
    unittest.main()
