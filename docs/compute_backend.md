# Compute backend and stronger-machine handoff

The current GAT, temporal transformer, simulator, and optimizer are pure NumPy
CPU implementations. Cloning this repository onto a machine with an NVIDIA
RTX GPU provides more storage and CPU/RAM headroom, but it does **not** make
these models use CUDA automatically. `upg-preflight` inventories an available
NVIDIA device through `nvidia-smi` while reporting the implemented backend
honestly as NumPy CPU.

GPU acceleration is a future, separately gated work unit. It requires a
PyTorch/JAX/CUDA implementation, deterministic seed and dtype policy,
checkpoint conversion, numerical parity tolerances, metric parity on the
frozen Batch K fixtures, and an independent verifier. No GPU result may
replace a frozen CPU result until those parity gates pass.

The current CPU GAT also fails closed when standardized features or prediction
heads are non-finite, and when an exponential calculation overflows or yields
a non-finite point, interval, or gain. It deliberately does not clip these
values. Passing that arithmetic gate only means an output is finite; it does
not validate a finite extreme OOD estimate. A future applicability detector,
parameter-bound rule, or clipping policy must be preregistered and evaluated
independently rather than introduced as an undocumented numerical fix.

## Recorded dependency

- **Work unit:** `UPG-INFRA-GPU-01`
- **Status:** pending; not part of pre-study CPU hardening
- **Dependency:** freeze CPU fixtures and benchmark contract first
- **Acceptance:** CPU/GPU structural, checkpoint, prediction, metric, and seed
  parity within preregistered tolerances on Linux/WSL2; independent rerun
- **Prohibited shortcut:** treating `nvidia-smi` visibility as CUDA support or
  silently changing the implementation/backend during a benchmark

The portable Linux/WSL2 bootstrap is:

```bash
uv run --locked --extra dev --extra study upg-preflight
```

Public retrospective data can be kept in a sibling `upg-data` clone or an
arbitrary larger-volume path:

```bash
UPG_PUBLIC_DATA_ROOT=/mnt/upg-data/redistributable \
  uv run --locked --extra dev --extra study upg-preflight --require-data
```

`UPG_DATA_ROOT` is reserved for the external content-addressed study store;
it is never interpreted as the public-data clone. Restricted/DUA datasets are
deliberately outside preflight.
