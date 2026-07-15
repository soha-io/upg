import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
COMPOSER = REPO / "batches" / "J-eight-dimension-model" / "scripts" / "compose_greatgraph.py"


def test_composer_check_is_nonmutating_and_byte_exact():
    targets = [
        REPO / "registries" / "upg_greatgraph_nodes.csv",
        REPO / "registries" / "upg_greatgraph_edges.csv",
        REPO / "batches" / "J-eight-dimension-model" / "data" / "upg_greatgraph_nodes.csv",
        REPO / "batches" / "J-eight-dimension-model" / "data" / "upg_greatgraph_edges.csv",
    ]
    before = [path.read_bytes() for path in targets]
    proc = subprocess.run(
        [sys.executable, str(COMPOSER), "--check"],
        cwd=REPO,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "byte parity" in proc.stdout
    assert [path.read_bytes() for path in targets] == before
