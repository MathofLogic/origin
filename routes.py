"""
ROUTES — two ways to arithmetic, and the wall they share.
==========================================================================
This repo holds two independent constructions of the same arithmetic.

  THE AXIOMATIC ROUTE (Peano).  Posit 0. Posit a successor. Define + and x
  by recursion on the successor. Add induction to fix which structure you
  meant. Arithmetic follows.

  THE MECHANISM ROUTE (closure).  Posit a pattern that returns to itself.
  Ask what it can distinguish. Addition is two patterns propagated
  together; multiplication is one pattern propagated repeatedly; the
  modular structure is the closure itself; the unbounded integers are the
  limit of refusing to close.

The interesting question is NOT which route is correct. Both produce the
same arithmetic, and this file checks that they agree. The question is
WHAT EACH ONE HAD TO ASSUME, and where each one stops.

THE HONEST RESULT, STATED BEFORE THE EVIDENCE
---------------------------------------------
The mechanism route assumes LESS: one primitive instead of five axioms,
and it DERIVES successor, addition and multiplication rather than
positing or defining them.

It does not assume NOTHING. A closure is a stipulation. Something had to
be held apart well enough to return to itself, and this repo does not
price that.

So the mechanism route TRADES a larger stipulation for a smaller one. It
does not escape stipulation, and claiming it did would be exactly the
reification both routes exist to expose.

And both routes hit the SAME wall at the same place: a finite check
cannot certify an unbounded claim. Peano closes that gap with induction,
a schema — an infinite family of axioms. The mechanism route has no
better answer, and says so.

Running this file IS its audit.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims import Suite
from closure import Closure, co_propagate, iterate
from peano_carrier import Nat, Z, S, nat, add, mul


# ── the mechanism route, unbounded reading ───────────────────────────
def m_add(a, b):
    """Two patterns propagated together, read at a closure large enough
    not to wrap. This is the limit of refusing to close."""
    C = Closure(max(a + b, 1) + 1)
    return co_propagate(C, a, b)


def m_mul(a, b):
    """One pattern propagated repeatedly."""
    C = Closure(max(a * b, 1) + 1)
    return iterate(C, a, b)


def m_succ(a):
    """Successor is not primitive here. It is co-propagation with the
    smallest non-loadless pattern."""
    return m_add(a, 1)


# ── the axiomatic route, read back as integers ───────────────────────
def p_add(a, b):
    return int(add(nat(a), nat(b)))


def p_mul(a, b):
    return int(mul(nat(a), nat(b)))


def p_succ(a):
    return int(S(nat(a)))


def audit():
    S_ = Suite("ROUTES — mechanism and axiom, compared", __file__)
    N = range(0, 9)
    CUT = f"all pairs from {{0..{max(N)}}}"

    # ── 1. the two routes agree ──────────────────────────────────────
    n_add = n_mul = n_succ = 0
    ok_add = ok_mul = ok_succ = True
    for a in N:
        n_succ += 1
        ok_succ &= (m_succ(a) == p_succ(a))
        for b in N:
            n_add += 1
            ok_add &= (m_add(a, b) == p_add(a, b))
            n_mul += 1
            ok_mul &= (m_mul(a, b) == p_mul(a, b))

    S_.add("SUCCESSOR AGREES: co-propagation with the smallest non-loadless "
           "pattern gives exactly Peano's successor — which the mechanism "
           "route derives rather than posits",
           ok_succ, n_succ, n_succ, True,
           "exhibit a value where derived successor differs from Peano's",
           f"{{0..{max(N)}}}")
    S_.add("ADDITION AGREES: two patterns propagated together give exactly "
           "Peano's recursively defined sum", ok_add, n_add, n_add, True,
           "exhibit a pair where co-propagation differs from Peano addition",
           CUT)
    S_.add("MULTIPLICATION AGREES: one pattern propagated repeatedly gives "
           "exactly Peano's recursively defined product — and it is NOT a "
           "second operation on either route", ok_mul, n_mul, n_mul, True,
           "exhibit a pair where repeated propagation differs from Peano "
           "multiplication", CUT)
    S_.seal({"stage": "agreement", "checks": n_add + n_mul + n_succ})

    # ── 2. what each route had to assume ────────────────────────────
    PEANO_POSITS = ["0 exists", "successor exists", "successor is injective",
                    "0 is not a successor", "induction (a schema)",
                    "addition by two recursion equations",
                    "multiplication by two recursion equations"]
    MECH_POSITS = ["a pattern that returns to itself"]
    S_.add(f"THE STIPULATION COUNT DIFFERS: the axiomatic route posits "
           f"{len(PEANO_POSITS)} things; the mechanism route posits "
           f"{len(MECH_POSITS)}. Successor, addition and multiplication move "
           "from the posited column to the derived column",
           len(MECH_POSITS) < len(PEANO_POSITS),
           len(PEANO_POSITS) + len(MECH_POSITS),
           len(PEANO_POSITS) + len(MECH_POSITS), True,
           "exhibit something the mechanism route posits that is not the "
           "closure", "the two stipulation lists")

    S_.add("THE MECHANISM ROUTE DOES NOT ASSUME NOTHING: a closure is a "
           "stipulation. It trades a larger assumption for a smaller one and "
           "does not escape assumption. Claiming otherwise would be the "
           "reification both routes exist to expose",
           len(MECH_POSITS) > 0, 0, None, False,
           "derive the closure primitive from something that is not itself "
           "stipulated", derived=True)

    # ── 3. the shared wall ──────────────────────────────────────────
    comm = all(m_add(a, b) == m_add(b, a) for a in N for b in N)
    S_.add("BOTH ROUTES HIT THE SAME WALL: commutativity of addition holds "
           f"for every pair in {CUT}. That is FORCED-on-cut and not FORCED. "
           "The value space is unbounded and the check is finite. Peano "
           "closes the gap with induction — a SCHEMA, one axiom per "
           "predicate, an infinite family that no enumeration closes. The "
           "mechanism route has no better answer",
           comm, n_add, n_add, True,
           "exhibit a pair in the cut where addition fails to commute", CUT)

    S_.nonclaim("NOT claimed: that the mechanism route grounds arithmetic. "
                "It relocates the stipulation and makes it smaller. "
                "Grounding from inside trades upward; it does not "
                "terminate.")
    S_.nonclaim("NOT claimed: that Peano's axioms are wrong. They are "
                "visible AS stipulations, and their consequences are forced. "
                "That is what an axiom set is for.")
    S_.nonclaim("NOT claimed: that agreement on a finite cut establishes "
                "agreement everywhere. Both routes are checked on "
                f"{CUT} and the lift is UNPAID.")
    S_.nonclaim("NOT claimed: any priority for the derived results. Several "
                "coincide with standard mathematics. Reaching established "
                "results by an independent route is confirmation that the "
                "route works, not a discovery.")
    return S_


if __name__ == "__main__":
    S_ = audit()
    S_.report()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "manifests", "routes_manifest.json"), "w") as f:
        json.dump(S_.manifest(), f, indent=2, sort_keys=True)
    sys.exit(1 if S_.failed() else 0)
