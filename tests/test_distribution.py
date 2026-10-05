# SPDX-License-Identifier: AGPL-3.0-or-later

"""Exercise built distributions without Bluetooth hardware.

Run with: python -m unittest discover -s tests -v
Requires build, setuptools, wheel, and the project's runtime dependencies.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.work = Path(temporary.name)
        source = cls.work / 'source'
        source.mkdir()
        for name in ('setup.py', 'README.md', 'LICENSE'):
            shutil.copy2(ROOT / name, source / name)
        shutil.copytree(
            ROOT / 'qingping', source / 'qingping',
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'),
        )
        cls.expected = {
            path.relative_to(source).as_posix()
            for path in (source / 'qingping').rglob('*.py')
        }
        distribution = cls.work / 'dist'
        cls.run_command([
            sys.executable, '-m', 'build', '--no-isolation',
            '--outdir', str(distribution), str(source),
        ])
        cls.wheel, = distribution.glob('*.whl')
        cls.sdist, = distribution.glob('*.tar.gz')
        cls.installed = cls.work / 'installed'
        cls.run_command([
            sys.executable, '-m', 'pip', 'install', '--no-deps', '--no-index',
            '--target', str(cls.installed), str(cls.wheel),
        ])

    @classmethod
    def run_command(cls, command):
        result = subprocess.run(
            command, cwd=cls.work, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stdout)
        return result.stdout

    def test_wheel_contains_all_package_modules(self):
        with zipfile.ZipFile(self.wheel) as archive:
            self.assertEqual(self.expected - set(archive.namelist()), set())

    def test_sdist_contains_all_package_modules(self):
        with tarfile.open(self.sdist) as archive:
            members = {
                name.partition('/')[2] for name in archive.getnames()
            }
            self.assertEqual(self.expected - members, set())

    def test_installed_modules_import_outside_source_tree(self):
        modules = []
        for path in sorted(self.expected):
            module = path[:-3].replace('/', '.')
            if module.endswith('.__init__'):
                module = module[:-len('.__init__')]
            modules.append(module)
        self.run_command([
            sys.executable, '-I', '-c',
            'import importlib, pathlib, sys; '
            'root = pathlib.Path(sys.argv[1]).resolve(); '
            'sys.path.insert(0, str(root)); '
            'modules = ' + json.dumps(modules) + '; '
            'origins = [pathlib.Path(importlib.import_module(name).__file__)'
            '.resolve() for name in modules]; '
            'assert all(root in origin.parents for origin in origins), origins',
            str(self.installed),
        ])

    def test_installed_bluetooth_cli_help(self):
        output = self.run_command([
            sys.executable, '-I', '-c',
            'import runpy, sys; '
            'sys.path.insert(0, sys.argv[1]); '
            'sys.argv = ["qingping.bluetooth", "--help"]; '
            'runpy.run_module("qingping.bluetooth", run_name="__main__")',
            str(self.installed),
        ])
        self.assertIn('qingping bluetooth configuration tool', output)
        self.assertIn('--mac', output)


if __name__ == '__main__':
    unittest.main()
