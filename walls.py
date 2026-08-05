"""
WALLS — where derivation stops, on BOTH routes, exhibited not hidden.
==========================================================================
Adapted from the peano repo, and generalised: these walls were originally
stated against the axiomatic route, and every one of them applies to the
mechanism route identically. That is the finding worth having. Deriving
successor and addition from a closure moves the stipulation; it does not
move the wall.

Running this file IS its audit.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims import Suite
from closure import Closure, co_propagate
from peano_carrier import Nat, Z, S, nat, add, mul


def audit():
    Su = Suite("WALLS — where both routes stop", __file__)

    # ── WALL 1 — the induction wall ─────────────────────────────────
    N = range(0, 7)
    held = all(int(add(nat(a), nat(b))) == int(add(nat(b), nat(a)))
               for a in N for b in N)
    n = len(N) ** 2
    Su.add("WALL 1 — INDUCTION. Commutativity held for every pair in "
           f"{{0..{max(N)}}}. That is evidence over a finite cut, not proof "
           "over an unbounded space. Closing the gap requires induction, "
           "which is a SCHEMA — one axiom per predicate, infinitely many. "
           "No enumeration closes an infinite axiom family, on either route",
           held, n, n, True,
           "exhibit a finite enumeration that certifies an unbounded "
           "universal without an induction schema", f"pairs in {{0..{max(N)}}}")

    # ── WALL 1b — the intruder ──────────────────────────────────────
    # A structure satisfying the first four axioms that is NOT the naturals.
    class ZLine:
        """Standard naturals with an extra disconnected Z-chain bolted on.
        Satisfies: has a zero, has an injective successor, zero is not a
        successor. Fails only induction."""
        def __init__(self, tag, k): self.tag, self.k = tag, k
        def succ(self): return ZLine(self.tag, self.k + 1)
        def __eq__(o, s): return (o.tag, o.k) == (s.tag, s.k)
        def __hash__(s): return hash((s.tag, s.k))

    zero = ZLine("N", 0)
    intruder = ZLine("Z", 0)          # not reachable from zero by successor
    reachable = {zero}
    cur = zero
    for _ in range(50):
        cur = cur.succ(); reachable.add(cur)
    escapes = intruder not in reachable
    inj = all(ZLine("N", i).succ() != ZLine("N", j).succ()
              for i in range(5) for j in range(5) if i != j)
    not_succ = all(zero != ZLine("N", i).succ() for i in range(5))
    Su.add("WALL 1b — THE INTRUDER. A structure with a disconnected extra "
           "chain satisfies zero-exists, successor-is-injective and "
           "zero-is-not-a-successor, yet contains elements no amount of "
           "succeeding from zero ever reaches. Only induction rules it out. "
           "This is what the schema is BUYING, made visible",
           escapes and inj and not_succ, 3, 3, True,
           "exhibit a first-order axiom, not a schema, that excludes this "
           "structure", "one intruder, three axioms")

    # ── WALL 2 — the Gödel wall ─────────────────────────────────────
    Su.add("WALL 2 — GROUNDING FROM INSIDE. A sufficiently strong "
           "arithmetic cannot prove its own consistency from within. "
           "Gentzen's proof exists and buys consistency at the price of a "
           "stronger assumption elsewhere — transfinite induction to "
           "epsilon-nought. That is a TRADE, not a grounding, and it is the "
           "same shape as the closure trade in routes.py",
           True, 0, None, False,
           "exhibit a consistency proof for a sufficiently strong "
           "arithmetic carried out entirely within it", derived=True)

    # ── WALL 3 — the wall the mechanism route adds ──────────────────
    C = Closure(7)
    closes = all(co_propagate(C, a, b) in range(7)
                 for a in range(7) for b in range(7))
    Su.add("WALL 3 — THE CLOSURE IS UNPRICED. Every mechanism-route result "
           "requires a pattern held apart well enough to return to itself. "
           "The propagation closes, which is checkable; the ESTABLISHING of "
           "the closure is not priced and cannot be, from inside. This is "
           "the mechanism route's own floor and it is the direct analogue "
           "of Wall 2",
           closes, 49, 49, True,
           "price the establishing of a closure using only resources "
           "downstream of that closure", "closure of 7, all pairs")

    Su.nonclaim("NOT claimed: that these walls are defects. They are the "
                "specification. A framework that hid them would be less "
                "useful, not more grounded.")
    Su.nonclaim("NOT claimed: that the walls are exhaustive. Four are "
                "exhibited.")
    Su.nonclaim("NOT claimed: that Wall 2 is proved here. It is cited, and "
                "cited claims cannot reach FORCED because the referent sits "
                "outside this artifact.")
    return Su


if __name__ == "__main__":
    Su = audit()
    Su.report()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "manifests", "walls_manifest.json"), "w") as f:
        json.dump(Su.manifest(), f, indent=2, sort_keys=True)
    sys.exit(1 if Su.failed() else 0)
