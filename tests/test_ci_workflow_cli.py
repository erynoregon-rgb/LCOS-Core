from pathlib import Path
import unittest


class CIWorkflowCliTest(unittest.TestCase):
    def test_ci_smoke_uses_public_cli_module(self) -> None:
        workflow = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
        content = workflow.read_text(encoding="utf-8")

        self.assertIn("python -m lcos_public.cli demo-ledger", content)
        self.assertNotIn("python -m lcos_toy.cli", content)
