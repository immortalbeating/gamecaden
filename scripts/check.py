"""Validate source, contracts and the selected regression suite in this checkout."""
from __future__ import annotations
import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'plugins/gamecaden'
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.path.insert(0, str(BUNDLE / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))

def run(command):
    return subprocess.run(command, cwd=ROOT).returncode == 0

def regression(pattern):
    suite = unittest.TestLoader().discover(str(ROOT / 'tests'), pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=['all', 'core', 'distribution'], default='all')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('distribution', BUNDLE / 'scripts/gamecaden.py')
    dist = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dist)
    dist.verify(BUNDLE)
    if not run([sys.executable, '-B', '-X', 'utf8', str(BUNDLE / 'scripts/check_contracts.py')]):
        return 1
    if args.suite in {'all', 'core'} and not regression('test_workflow*.py'):
        return 1
    if args.suite in {'all', 'distribution'} and not regression('test_gamecaden*.py'):
        return 1
    if args.suite == 'all':
        node = shutil.which('node')
        if not node:
            parser.error('Node.js is needed for --suite all (JavaScript regression).')
        if not run([node, '--test', str(ROOT / 'tests/test_panel_refresh.mjs')]):
            return 1
        (ROOT / 'dist').mkdir(exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix='rebuild-', dir=ROOT / 'dist'))
        first = dist.build(BUNDLE, folder / 'a')
        second = dist.build(BUNDLE, folder / 'b')
        assert first['digest'] == second['digest']
        assert first['archive_sha256'] == second['archive_sha256']
        assert (Path(first['plugin_root']) / 'LICENSE').is_file()
    print('PASS: selected checks completed in this repository; no game or model execution.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
