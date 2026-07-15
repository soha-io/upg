from pathlib import Path

import pytest

from upg.data_paths import (PUBLIC_REQUIRED, PublicDataLayoutError,
                            resolve_public_data_root)


def _public_layout(root: Path) -> Path:
    for relative in PUBLIC_REQUIRED:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
    return root


def test_explicit_public_root_has_precedence(tmp_path):
    explicit = _public_layout(tmp_path / "explicit")
    env = _public_layout(tmp_path / "env")
    resolved = resolve_public_data_root(
        repo_root=tmp_path / "repo",
        explicit=explicit,
        environ={"UPG_PUBLIC_DATA_ROOT": str(env), "UPG_DATA_ROOT": "/cas"},
    )
    assert resolved == explicit.resolve()


def test_public_env_precedes_sibling_and_cas_is_ignored(tmp_path):
    repo = tmp_path / "project" / "upg"
    env = _public_layout(tmp_path / "public")
    _public_layout(repo.parent / "upg-data" / "redistributable")
    resolved = resolve_public_data_root(
        repo_root=repo,
        environ={"UPG_PUBLIC_DATA_ROOT": str(env), "UPG_DATA_ROOT": "/external/cas"},
    )
    assert resolved == env.resolve()


def test_invalid_explicit_or_env_fails_without_fallback(tmp_path):
    repo = tmp_path / "project" / "upg"
    _public_layout(repo.parent / "upg-data" / "redistributable")
    with pytest.raises(PublicDataLayoutError, match="--data-root"):
        resolve_public_data_root(
            repo_root=repo, explicit=tmp_path / "bad", environ={}
        )
    bad_env = tmp_path / "bad-env"
    bad_env.mkdir()
    with pytest.raises(PublicDataLayoutError, match="UPG_PUBLIC_DATA_ROOT.*invalid"):
        resolve_public_data_root(
            repo_root=repo, environ={"UPG_PUBLIC_DATA_ROOT": str(bad_env)}
        )


def test_absent_sibling_is_optional_only_when_requested(tmp_path):
    repo = tmp_path / "project" / "upg"
    assert resolve_public_data_root(
        repo_root=repo, environ={}, allow_absent_sibling=True
    ) is None
    with pytest.raises(PublicDataLayoutError, match="public data not found"):
        resolve_public_data_root(repo_root=repo, environ={})
