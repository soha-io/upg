"""
Minimal reverse-mode automatic differentiation on NumPy arrays.

This is the shared substrate for the Phase-2 deep estimators (Step 5 GAT,
Step 6 transformer).  Design rules, inherited from the project charter and
the transformer reading notes:

  * **Exact, not approximate** (note 23's policy): plain float64 NumPy, no
    stochastic kernels, no fused approximations.  Two runs with the same seed
    produce bit-identical results.
  * **Small surface, fully gradchecked** (requirement 21): only the ops the
    two models need exist, and every op's gradient is verified against
    central finite differences in ``tests/test_autodiff.py``.
  * **No framework dependency** (requirements 17/18): the entire deep stack
    stays inside the project's own audited code — the models remain
    hand-inspectable objects, not opaque library modules.

The API is a deliberately tiny subset of the familiar tensor interface:

    >>> a = Tensor(np.ones((2, 3)), requires_grad=True)
    >>> y = (a * 2.0 + 1.0).tanh().sum()
    >>> y.backward()
    >>> a.grad.shape
    (2, 3)

Broadcasting follows NumPy; gradients are un-broadcast (summed) back to each
operand's shape.  ``matmul`` supports batched operands of ndim >= 2.
"""
from __future__ import annotations

import numpy as np

__all__ = ["Tensor", "Adam", "concat", "softmax_masked", "rms_norm",
           "gradcheck"]


def _unbroadcast(grad: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    """Sum ``grad`` down to ``shape`` (reverse of NumPy broadcasting)."""
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for ax, s in enumerate(shape):
        if s == 1 and grad.shape[ax] != 1:
            grad = grad.sum(axis=ax, keepdims=True)
    return grad.reshape(shape)


class Tensor:
    """A NumPy array with a gradient and a backward graph."""

    __slots__ = ("data", "grad", "requires_grad", "_parents", "_backward")

    def __init__(self, data, requires_grad: bool = False):
        self.data = np.asarray(data, dtype=np.float64)
        self.grad: np.ndarray | None = None
        self.requires_grad = bool(requires_grad)
        self._parents: tuple[Tensor, ...] = ()
        self._backward = None

    # -- construction helpers ---------------------------------------------
    @staticmethod
    def _wrap(other) -> "Tensor":
        return other if isinstance(other, Tensor) else Tensor(other)

    def _make(self, data, parents, backward) -> "Tensor":
        out = Tensor(data)
        out.requires_grad = any(p.requires_grad for p in parents)
        if out.requires_grad:
            out._parents = tuple(parents)
            out._backward = backward
        return out

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    def detach(self) -> "Tensor":
        return Tensor(self.data.copy())

    # -- arithmetic ---------------------------------------------------------
    def __add__(self, other):
        other = self._wrap(other)

        def backward(g, a=self, b=other):
            if a.requires_grad:
                a._accum(_unbroadcast(g, a.shape))
            if b.requires_grad:
                b._accum(_unbroadcast(g, b.shape))
        return self._make(self.data + other.data, (self, other), backward)

    __radd__ = __add__

    def __mul__(self, other):
        other = self._wrap(other)

        def backward(g, a=self, b=other):
            if a.requires_grad:
                a._accum(_unbroadcast(g * b.data, a.shape))
            if b.requires_grad:
                b._accum(_unbroadcast(g * a.data, b.shape))
        return self._make(self.data * other.data, (self, other), backward)

    __rmul__ = __mul__

    def __neg__(self):
        def backward(g, a=self):
            if a.requires_grad:
                a._accum(-g)
        return self._make(-self.data, (self,), backward)

    def __sub__(self, other):
        return self + (-self._wrap(other))

    def __rsub__(self, other):
        return self._wrap(other) + (-self)

    def __truediv__(self, other):
        return self * self._wrap(other).pow(-1.0)

    def __rtruediv__(self, other):
        return self._wrap(other) * self.pow(-1.0)

    def pow(self, p: float) -> "Tensor":
        out_data = self.data ** p

        def backward(g, a=self, p=p, od=out_data):
            if a.requires_grad:
                a._accum(g * p * a.data ** (p - 1.0))
        return self._make(out_data, (self,), backward)

    def matmul(self, other: "Tensor") -> "Tensor":
        other = self._wrap(other)
        if self.ndim < 2 or other.ndim < 2:
            raise ValueError("matmul requires ndim >= 2 operands")

        def backward(g, a=self, b=other):
            if a.requires_grad:
                ga = g @ np.swapaxes(b.data, -1, -2)
                a._accum(_unbroadcast(ga, a.shape))
            if b.requires_grad:
                gb = np.swapaxes(a.data, -1, -2) @ g
                b._accum(_unbroadcast(gb, b.shape))
        return self._make(self.data @ other.data, (self, other), backward)

    __matmul__ = matmul

    # -- elementwise nonlinearities ----------------------------------------
    def exp(self) -> "Tensor":
        out_data = np.exp(self.data)

        def backward(g, a=self, od=out_data):
            if a.requires_grad:
                a._accum(g * od)
        return self._make(out_data, (self,), backward)

    def log(self) -> "Tensor":
        def backward(g, a=self):
            if a.requires_grad:
                a._accum(g / a.data)
        return self._make(np.log(self.data), (self,), backward)

    def tanh(self) -> "Tensor":
        out_data = np.tanh(self.data)

        def backward(g, a=self, od=out_data):
            if a.requires_grad:
                a._accum(g * (1.0 - od ** 2))
        return self._make(out_data, (self,), backward)

    def sigmoid(self) -> "Tensor":
        out_data = 1.0 / (1.0 + np.exp(-self.data))

        def backward(g, a=self, od=out_data):
            if a.requires_grad:
                a._accum(g * od * (1.0 - od))
        return self._make(out_data, (self,), backward)

    def silu(self) -> "Tensor":
        """x * sigmoid(x) — the SwiGLU gate nonlinearity (note 32)."""
        s = 1.0 / (1.0 + np.exp(-self.data))
        out_data = self.data * s

        def backward(g, a=self, s=s):
            if a.requires_grad:
                a._accum(g * (s * (1.0 + a.data * (1.0 - s))))
        return self._make(out_data, (self,), backward)

    def softplus(self) -> "Tensor":
        """log(1 + exp(x)), numerically stable."""
        out_data = np.logaddexp(0.0, self.data)

        def backward(g, a=self):
            if a.requires_grad:
                a._accum(g / (1.0 + np.exp(-a.data)))
        return self._make(out_data, (self,), backward)

    def leaky_relu(self, alpha: float = 0.2) -> "Tensor":
        mask = (self.data > 0).astype(np.float64)
        slope = mask + alpha * (1.0 - mask)

        def backward(g, a=self, slope=slope):
            if a.requires_grad:
                a._accum(g * slope)
        return self._make(self.data * slope, (self,), backward)

    # -- reductions / reshaping ---------------------------------------------
    def sum(self, axis=None, keepdims: bool = False) -> "Tensor":
        out_data = self.data.sum(axis=axis, keepdims=keepdims)

        def backward(g, a=self, axis=axis, keepdims=keepdims):
            if not a.requires_grad:
                return
            gg = np.asarray(g)
            if axis is not None and not keepdims:
                gg = np.expand_dims(gg, axis)
            a._accum(np.broadcast_to(gg, a.shape).copy())
        return self._make(out_data, (self,), backward)

    def mean(self, axis=None, keepdims: bool = False) -> "Tensor":
        n = self.data.size if axis is None else self.data.shape[axis]
        return self.sum(axis=axis, keepdims=keepdims) * (1.0 / n)

    def reshape(self, *shape) -> "Tensor":
        old = self.shape

        def backward(g, a=self, old=old):
            if a.requires_grad:
                a._accum(g.reshape(old))
        return self._make(self.data.reshape(*shape), (self,), backward)

    def transpose(self, axes) -> "Tensor":
        inv = np.argsort(axes)

        def backward(g, a=self, inv=inv):
            if a.requires_grad:
                a._accum(g.transpose(inv))
        return self._make(self.data.transpose(axes), (self,), backward)

    def __getitem__(self, key) -> "Tensor":
        def backward(g, a=self, key=key):
            if a.requires_grad:
                out = np.zeros_like(a.data)
                np.add.at(out, key, g)
                a._accum(out)
        return self._make(self.data[key], (self,), backward)

    # -- autodiff engine -----------------------------------------------------
    def _accum(self, g: np.ndarray) -> None:
        self.grad = g if self.grad is None else self.grad + g

    def backward(self) -> None:
        if self.data.size != 1:
            raise ValueError("backward() requires a scalar output")
        topo: list[Tensor] = []
        seen: set[int] = set()

        def visit(t: Tensor) -> None:
            if id(t) in seen or not t.requires_grad:
                return
            seen.add(id(t))
            for p in t._parents:
                visit(p)
            topo.append(t)

        visit(self)
        self.grad = np.ones_like(self.data)
        for t in reversed(topo):
            if t._backward is not None:
                t._backward(t.grad)


# ==========================================================================
# Composite building blocks
# ==========================================================================


def concat(tensors: list[Tensor], axis: int = -1) -> Tensor:
    """Concatenate along ``axis`` with gradient splitting."""
    datas = [t.data for t in tensors]
    out = Tensor(np.concatenate(datas, axis=axis))
    out.requires_grad = any(t.requires_grad for t in tensors)
    if out.requires_grad:
        sizes = [d.shape[axis] for d in datas]
        splits = np.cumsum(sizes)[:-1]

        def backward(g, tensors=tuple(tensors), splits=splits, axis=axis):
            parts = np.split(g, splits, axis=axis)
            for t, p in zip(tensors, parts):
                if t.requires_grad:
                    t._accum(p)
        out._parents = tuple(tensors)
        out._backward = backward
    return out


def softmax_masked(logits: Tensor, mask: np.ndarray | None = None,
                   axis: int = -1) -> Tensor:
    """Softmax along ``axis``; positions with mask==0 receive ~zero weight.

    The mask is a constant array (not differentiated).  The max-subtraction
    stabilizer is detached, as is standard.
    """
    x = logits
    if mask is not None:
        neg = np.where(mask > 0, 0.0, -1e9)
        x = x + Tensor(neg)
    m = np.max(x.data, axis=axis, keepdims=True)
    e = (x - Tensor(m)).exp()
    if mask is not None:
        e = e * Tensor((mask > 0).astype(np.float64))
    denom = e.sum(axis=axis, keepdims=True) + 1e-12
    return e / denom


def rms_norm(x: Tensor, gamma: Tensor, eps: float = 1e-6) -> Tensor:
    """RMSNorm over the last axis (note 31): x / RMS(x) * gamma."""
    ms = (x * x).mean(axis=-1, keepdims=True)
    return x * (ms + eps).pow(-0.5) * gamma


# ==========================================================================
# Optimizer
# ==========================================================================


class Adam:
    """Standard Adam over a list of parameter Tensors (deterministic)."""

    def __init__(self, params: list[Tensor], lr: float = 3e-3,
                 beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self.params = list(params)
        self.lr, self.b1, self.b2, self.eps = lr, beta1, beta2, eps
        self.m = [np.zeros_like(p.data) for p in self.params]
        self.v = [np.zeros_like(p.data) for p in self.params]
        self.t = 0

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            if p.grad is None:
                continue
            g = p.grad
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            p.data -= self.lr * mh / (np.sqrt(vh) + self.eps)


# ==========================================================================
# Verification
# ==========================================================================


def gradcheck(fn, tensors: list[Tensor], eps: float = 1e-6,
              tol: float = 1e-4) -> float:
    """Compare analytic gradients of scalar ``fn(*tensors)`` with central
    finite differences.  Returns the worst relative error found."""
    for t in tensors:
        t.grad = None
    out = fn(*tensors)
    out.backward()
    worst = 0.0
    for t in tensors:
        it = np.nditer(t.data, flags=["multi_index"])
        while not it.finished:
            ix = it.multi_index
            orig = t.data[ix]
            t.data[ix] = orig + eps
            f_hi = float(fn(*tensors).data)
            t.data[ix] = orig - eps
            f_lo = float(fn(*tensors).data)
            t.data[ix] = orig
            num = (f_hi - f_lo) / (2 * eps)
            ana = float(t.grad[ix]) if t.grad is not None else 0.0
            denom = max(1.0, abs(num), abs(ana))
            worst = max(worst, abs(num - ana) / denom)
            it.iternext()
    if worst > tol:
        raise AssertionError(f"gradcheck failed: worst rel err {worst:.2e}")
    return worst
