"""
peano_carrier.py — Peano arithmetic as a PL carrier, de-reified.
==========================================================================
THE DE-REIFICATION, STATED FIRST so nothing downstream can smuggle it:

Peano Arithmetic is usually taught as a DISCOVERY — "here are the natural
numbers, here are the true facts about them." PL reads it as a CHOICE:

    V (value space)  : whatever the successor operator generates from 0
    G (operators)    : successor S, then + and x DEFINED (not discovered)
                       by recursion on S
    theta            : the induction schema — the stipulation that fixes
                       WHICH structure counts, ruling out the intruders

Nothing here is "the numbers as they really are." Each axiom is a
constraint; the arithmetic is what those constraints FORCE. We derive
+ and x from S by their recursion equations and CHECK the ring-ish laws
by enumeration on a finite cut of the carrier. Then we exhibit the two
walls where enumeration cannot follow and PL must hand off to citation:
  (1) induction is a schema over an unbounded V — no finite check closes it
  (2) Con(PA) is not provable inside PA (Godel) — de-reifying the axioms
      does not, and cannot, ground them from inside.

The point is NOT "PL grounds arithmetic." That would reify PL. The point
is: the axioms are visible AS stipulations, their consequences are
FORCED and checkable, and the exact seam where grounding stops is named
out loud instead of papered over.
"""
from __future__ import annotations
from dataclasses import dataclass

# --- V: the value space is GENERATED, not presupposed --------------------
# A natural number is not an atom "out there"; it is a finite tower of S
# over Z. We build the tower explicitly so V is visibly a construction.

@dataclass(frozen=True)
class Nat:
    """0 is Z(); n+1 is S(n). The number IS its construction history."""
    pred: "Nat | None"  # None == zero

    def __repr__(self):
        return f"S^{int(self)}(0)"

    def __int__(self):
        n, x = 0, self
        while x.pred is not None:
            n, x = n + 1, x.pred
        return n

Z = Nat(None)                      # axiom 1: 0 is a number
def S(n: Nat) -> Nat:              # axiom 2: successor of a number is a number
    return Nat(n)

def nat(k: int) -> Nat:            # convenience: build S^k(0)
    x = Z
    for _ in range(k):
        x = S(x)
    return x


# --- G: + and x are DEFINED by recursion on S, not assumed ---------------
# This is the crux of de-reification. Addition is not a primitive fact
# about numbers; it is an OPERATOR we install by two equations. Change the
# equations and you change the carrier.

def add(a: Nat, b: Nat) -> Nat:
    # a + 0 = a  ;  a + S(b) = S(a + b)
    if b.pred is None:
        return a
    return S(add(a, b.pred))

def mul(a: Nat, b: Nat) -> Nat:
    # a * 0 = 0  ;  a * S(b) = (a * b) + a
    if b.pred is None:
        return Z
    return add(mul(a, b.pred), a)


# --- the Peano axioms, each stated AS A STIPULATION ----------------------
AXIOMS = {
    "P1": "0 is a number.  (Z exists — a chosen origin, not a found one)",
    "P2": "every number has a successor S(n).  (V is closed under S)",
    "P3": "0 is not a successor: S(n) != 0.  (the tower has a floor)",
    "P4": "S is injective: S(m)=S(n) => m=n.  (no two towers merge)",
    "P5": "INDUCTION: if P(0) and (P(n)=>P(S(n))) then P(n) for all n. "
          "(the theta — it FIXES the intended structure and forbids "
          "extra 'numbers' not reachable from 0 by S)",
}
