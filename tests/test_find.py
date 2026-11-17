import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/work-unit/scripts/find.sh"
EXAMPLE = json.loads((ROOT / "docs/resources/work-unit.example.json").read_text())


class FindTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="work-unit tests ")
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name).resolve()
        self.registry = self.project / ".agents/work-units"
        self.registry.mkdir(parents=True)

    def invoke(self, reference="DEMO-42", **kwargs):
        return subprocess.run(
            [str(SCRIPT), str(self.project), reference],
            capture_output=True,
            text=True,
            **kwargs,
        )

    def write_unit(self, name="unit with spaces.json", unit=None):
        path = self.registry / name
        path.write_text(json.dumps(EXAMPLE if unit is None else unit))
        return path

    def test_empty_registry_and_no_match(self):
        self.assertEqual(json.loads(self.invoke().stdout), [])
        self.write_unit()
        result = self.invoke("unknown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_lookup_id_name_title_resources_participants_and_nested_links(self):
        path = self.write_unit()
        references = [
            EXAMPLE["id"], EXAMPLE["name"],
            "".join(EXAMPLE["emojis"]) + " " + EXAMPLE["name"],
            *[r["target"] for r in EXAMPLE["references"]],
            *[p["id"] for p in EXAMPLE["participants"]],
        ]
        for task in EXAMPLE["asana"]:
            references.extend(task[field] for field in ["task_gid", "key", "url"])
        for implementation in EXAMPLE["implementations"]:
            references.extend([
                implementation["repository_url"], implementation["branch"],
                *implementation["worktree_paths"], *implementation["merge_request_urls"],
            ])
        for reference in references:
            with self.subTest(reference=reference):
                result = self.invoke(reference)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), [{"file": str(path), "unit": EXAMPLE}])

    def test_ambiguous_matches_are_preserved(self):
        self.write_unit()
        other = copy.deepcopy(EXAMPLE)
        other["id"] = "1f3c8749-5b90-4d42-973d-dae3fd95c7eb"
        self.write_unit("other.json", other)
        self.assertEqual(len(json.loads(self.invoke().stdout)), 2)

    def test_only_top_level_json_files_are_read(self):
        self.write_unit()
        (self.registry / "ignored.txt").write_text("invalid")
        (self.registry / "nested").mkdir()
        (self.registry / "nested/ignored.json").write_text("invalid")
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 1)

    def test_errors_have_no_partial_stdout(self):
        self.write_unit()
        (self.registry / "broken.json").write_text("{broken")
        for reference in ["DEMO-42", ""]:
            with self.subTest(reference=reference):
                result = self.invoke(reference)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
        result = subprocess.run([str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_missing_registry_is_an_error(self):
        self.registry.rmdir()
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_project_registries_are_isolated(self):
        other_registry = self.project / "another-project/.agents/work-units"
        other_registry.mkdir(parents=True)
        (other_registry / "unit.json").write_text(json.dumps(EXAMPLE))
        self.assertEqual(json.loads(self.invoke().stdout), [])

    def test_find_batches_produce_one_array(self):
        self.write_unit()
        self.write_unit("second.json")
        shims = self.project / "bin"
        shims.mkdir()
        # Make find invoke jq once per file to exercise batch aggregation.
        wrapper = shims / "find"
        wrapper.write_text(
            '#!/usr/bin/env bash\nargs=("$@")\n'
            'last=$((${#args[@]}-1))\nargs[$last]=";"\n'
            'exec /usr/bin/find "${args[@]}"\n'
        )
        wrapper.chmod(0o755)
        environment = dict(os.environ, PATH=str(shims) + os.pathsep + os.environ["PATH"])
        result = self.invoke(env=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 2)


if __name__ == "__main__":
    unittest.main()
