#!/usr/bin/env python3
"""
Zero-dependency test runner.

Use this when pytest is not installed.  It discovers ``test_*`` functions in
``tests/`` and runs them, reporting pass/fail per test.  Simple module-level
fixtures (``@pytest.fixture``) and ``tmp_path`` are resolved by a minimal
built-in resolver; modules that cannot be imported without pytest are
skipped with a notice.  When pytest *is* available, prefer ``pytest -q``
(the same test files are standard pytest).

    python run_tests.py
"""
from __future__ import annotations

import importlib.util
import inspect
import os
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
TESTS = os.path.join(ROOT, "tests")


def load_module(path: str):
    name = "t_" + os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fixture_func(obj):
    """Unwrap a @pytest.fixture-decorated object to its plain function."""
    if callable(obj) and hasattr(obj, "__wrapped__"):
        return obj.__wrapped__
    if hasattr(obj, "_fixture_function"):          # older/newer pytest APIs
        return obj._fixture_function
    return obj if callable(obj) else None


def resolve_args(fn, mod, cache: dict):
    """Resolve a test's parameters from module fixtures / tmp_path."""
    args = []
    for pname in inspect.signature(fn).parameters:
        if pname == "tmp_path":
            args.append(Path(tempfile.mkdtemp(prefix="upgtest_")))
            continue
        if pname in cache:
            args.append(cache[pname])
            continue
        raw = getattr(mod, pname, None)
        f = _fixture_func(raw)
        if f is None:
            raise RuntimeError(f"cannot resolve fixture {pname!r}")
        value = f()
        cache[pname] = value                       # module-scope caching
        args.append(value)
    return args


def main() -> int:
    files = sorted(f for f in os.listdir(TESTS)
                   if f.startswith("test_") and f.endswith(".py"))
    passed = failed = skipped = 0
    failures: list[str] = []
    for f in files:
        try:
            mod = load_module(os.path.join(TESTS, f))
        except ImportError as exc:
            print(f"  SKIP  {f} (unimportable here: {exc})")
            skipped += 1
            continue
        cache: dict = {}
        for name in sorted(dir(mod)):
            if not name.startswith("test_"):
                continue
            fn = getattr(mod, name)
            if not callable(fn):
                continue
            try:
                fn(*resolve_args(fn, mod, cache))
                passed += 1
                print(f"  PASS  {f}::{name}")
            except Exception:  # noqa: BLE001
                failed += 1
                failures.append(f"{f}::{name}\n{traceback.format_exc()}")
                print(f"  FAIL  {f}::{name}")
    print("-" * 60)
    print(f"{passed} passed, {failed} failed, {skipped} module(s) skipped")
    if failures:
        print("\n" + "=" * 60 + "\nFAILURE DETAIL\n" + "=" * 60)
        for d in failures:
            print(d)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
