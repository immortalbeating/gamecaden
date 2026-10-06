"""Fault injection for installation transactions; exclusively disposable fixtures."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import gamecaden as gc

BUNDLE = (Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
WORK = BUNDLE.parents[1] / "work/distribution-recovery"


class Recovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        WORK.mkdir(parents=True, exist_ok=True)
        cls.root = Path(tempfile.mkdtemp(prefix="suite-", dir=WORK))
        cls.package = gc.build(BUNDLE, cls.root / "release")["plugin_root"]

    def setUp(self):
        self.target = self.root / self._testMethodName

    def interrupted(self):
        real = gc.atomic
        def fail(path, data, **options):
            if path.name == "state.json":
                raise OSError("simulated process failure after catalog promotion")
            return real(path, data, **options)
        with patch.object(gc, "atomic", fail), self.assertRaises(OSError):
            gc.stage(self.package, self.target)

    def test_resume_after_catalog_promotion(self):
        self.interrupted()
        with self.assertRaises(gc.DistributionError) as caught:
            gc.status(self.target)
        self.assertEqual(caught.exception.code, "recovery_required")
        result = gc.recover(self.target)
        self.assertTrue(result["recovered"])
        self.assertEqual(result["current"]["digest"], gc.verify(self.package)["digest"])
        self.assertFalse(gc.recover(self.target)["recovered"])

    def test_recovery_preserves_external_catalog_edit(self):
        self.interrupted()
        catalog = self.target / ".agents/plugins/marketplace.json"
        value = json.loads(catalog.read_text(encoding="utf-8"))
        value["external-edit"] = True
        catalog.write_text(json.dumps(value), encoding="utf-8")
        before = catalog.read_bytes()
        with self.assertRaises(gc.DistributionError) as caught:
            gc.recover(self.target)
        self.assertEqual(caught.exception.code, "recovery_conflict")
        self.assertEqual(catalog.read_bytes(), before)
        self.assertTrue((self.target / ".gamecaden-install/transaction.json").is_file())

    def test_conflict_observed_at_final_replace_is_preserved(self):
        path = gc.safe_path(self.root / "replace.json")
        path.write_bytes(b"before")
        real_fsync = os.fsync
        def external_edit(fd):
            real_fsync(fd)
            path.write_bytes(b"external")
        with patch.object(gc.os, "fsync", external_edit), self.assertRaises(gc.DistributionError):
            gc.atomic(path, b"after", expected=b"before")
        self.assertEqual(path.read_bytes(), b"external")

    def test_locked_install_refuses_second_process(self):
        with gc.locked(gc.safe_path(self.target)):
            result = subprocess.run([sys.executable, str(BUNDLE / "scripts/gamecaden.py"), "stage",
                                     "--package", self.package, "--target-root", str(self.target)],
                                    capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["code"], "installation_busy")
        self.assertFalse((self.target / ".agents/plugins/marketplace.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
