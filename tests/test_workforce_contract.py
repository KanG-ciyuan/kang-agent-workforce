import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkforceContractTests(unittest.TestCase):
    def test_identity_matches_manifest(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["name"], "kang-agent-workforce")
        self.assertIn("name: kang-agent-workforce", skill)
        self.assertIn(f'version: "{manifest["version"]}"', skill)

    def test_root_has_one_discoverable_skill(self):
        entrypoints = list(ROOT.rglob("SKILL.md"))
        self.assertEqual(entrypoints, [ROOT / "SKILL.md"])

    def test_permission_and_handoff_gates_are_explicit(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contract = (ROOT / "contracts" / "handoff.schema.yaml").read_text(encoding="utf-8")
        self.assertIn("read-only baseline", skill)
        self.assertIn("human approval", skill)
        self.assertIn("default: read_only", contract)
        self.assertIn("requires_human_approval", contract)


if __name__ == "__main__":
    unittest.main()
