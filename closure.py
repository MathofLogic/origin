"""
THE PRIMITIVE.

A closure is a pattern that returns to itself. Nothing here is a number.
Numbers are what closures give you when you ask what they can distinguish.

Running this file IS its audit.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims import Suite


class Closure:
    """n distinguishable phase positions that return to themselves."""
    __slots__ = ("n",)
    def __init__(self, n):
        if n < 1: raise ValueError("a closure must close")
        self.n = n
    def positions(self): return range(self.n)
    def __repr__(self): return f"Closure({self.n})"


def co_propagate(C, a, b):
    """Two patterns propagated together. Windings compose; the closure wraps.
    This is addition — derived, not defined."""
    return (a + b) % C.n


def iterate(C, a, k):
    """The same pattern propagated k times. This is multiplication —
    repeated co-propagation, not a second operation."""
    out = 0
    for _ in range(k):
        out = co_propagate(C, out, a)
    return out


def inverse(C, a):
    """The pattern that undoes a under co-propagation."""
    return (-a) % C.n


def reversible(C, a):
    """Is there a pattern that undoes a under ITERATION (not composition)?"""
    return any(iterate(C, a, b) % C.n == 1 % C.n for b in range(C.n))


def annihilates(C, a, b):
    """Do two non-trivial patterns wholly cancel? Total mutual venting."""
    return a % C.n != 0 and b % C.n != 0 and (a * b) % C.n == 0


def audit():
    S = Suite("CLOSURE — the primitive", __file__)

    # co-propagation is associative, commutative, has identity and inverses
    NS = range(1, 25)
    n_assoc = n_comm = n_id = n_inv = 0
    ok_assoc = ok_comm = ok_id = ok_inv = True
    for n in NS:
        C = Closure(n)
        for a in C.positions():
            n_id += 1
            ok_id &= (co_propagate(C, a, 0) == a)
            n_inv += 1
            ok_inv &= (co_propagate(C, a, inverse(C, a)) == 0)
            for b in C.positions():
                n_comm += 1
                ok_comm &= (co_propagate(C, a, b) == co_propagate(C, b, a))
                for c in C.positions():
                    n_assoc += 1
                    ok_assoc &= (co_propagate(C, co_propagate(C, a, b), c)
                                 == co_propagate(C, a, co_propagate(C, b, c)))
    CUT = f"closures 1..{max(NS)}, all positions"
    S.add("co-propagation is associative", ok_assoc, n_assoc, n_assoc, True,
          "exhibit a closure and three patterns where grouping matters", CUT)
    S.add("co-propagation is commutative", ok_comm, n_comm, n_comm, True,
          "exhibit two patterns whose composition order changes the result",
          CUT)
    S.add("the loadless pattern is a two-sided identity", ok_id, n_id, n_id,
          True, "exhibit a pattern that winding-0 fails to leave unchanged",
          CUT)
    S.add("every pattern has an inverse propagation", ok_inv, n_inv, n_inv,
          True, "exhibit a pattern with no undoing partner", CUT)
    S.seal({"stage": "group-structure", "checks": n_assoc + n_comm})

    # iteration IS multiplication
    n_mul, ok_mul = 0, True
    for n in NS:
        C = Closure(n)
        for a in C.positions():
            for k in range(12):
                n_mul += 1
                ok_mul &= (iterate(C, a, k) == (a * k) % n)
    S.add("iteration equals multiplication: repeated co-propagation is not "
          "a second operation", ok_mul, n_mul, n_mul, True,
          "exhibit (closure, a, k) where repeated composition differs from "
          "the product", f"closures 1..{max(NS)}, k in 0..11")
    S.seal({"stage": "multiplication", "checks": n_mul})

    S.nonclaim("NOT claimed: that a closure is priced. Establishing an "
               "isolation is the floor of this framework and is not "
               "derived here.")
    S.nonclaim("NOT claimed: that these results hold past the enumerated "
               "closures. Lifting the quantifier requires induction — a "
               "schema, an infinite family — and that lift is not taken.")
    S.nonclaim("NOT claimed: that co-propagation is the only composition a "
               "closure admits. It is the one this suite enumerates.")
    return S


if __name__ == "__main__":
    S = audit()
    S.report()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "manifests", "closure_manifest.json"), "w") as f:
        json.dump(S.manifest(), f, indent=2, sort_keys=True)
    sys.exit(1 if S.failed() else 0)
