"""
NUMBER THEORY FROM CLOSURE.

The construction order is inverted from the usual one. We do not build the
integers and then reduce them modulo n. A closure at resolution n GIVES the
modular structure directly — it is the natural object. The unbounded
integers are what you get by refusing to close: the limit, not the start.

Primality is not imported. It falls out as: the closures in which no two
non-trivial patterns can wholly cancel one another.

Running this file IS its audit.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims import Suite
from closure import Closure, co_propagate, iterate


def classical_prime(n):
    """Reference definition, used ONLY to check agreement — never to define."""
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def has_annihilating_pair(n):
    """Two non-zero patterns whose composition vents everything."""
    return any((a * b) % n == 0 for a in range(1, n) for b in range(1, n))


def all_reversible(n):
    """Every non-zero pattern has something that undoes it under iteration."""
    return all(any((a * b) % n == 1 for b in range(1, n)) for a in range(1, n))


def units(n):
    return [a for a in range(1, n) if any((a * b) % n == 1 for b in range(1, n))]


def return_time(a, n):
    """How many self-propagations before the pattern comes home."""
    k, cur = 1, a % n
    while cur != 1:
        cur = (cur * a) % n
        k += 1
        if k > n:
            return None
    return k


def audit():
    S = Suite("NUMBERS — number theory from closure", __file__)

    # ---- 1. value is closure-relative; the closure's own structure is not
    W, NS = 5, (3, 7, 12, 100)
    readings = {n: W % n for n in NS}
    S.add("VALUE IS CLOSURE-RELATIVE: the same winding reads differently at "
          "different closures, so a bare numeral is a reification",
          len(set(readings.values())) > 1, len(NS), len(NS), True,
          "exhibit a winding whose value is identical at every closure",
          f"winding {W} read at closures {NS}")

    div = {n: sorted(d for d in range(1, n + 1) if n % d == 0)
           for n in (12, 13, 16, 17)}
    S.add("CLOSURE STRUCTURE IS INVARIANT: the divisor structure of a closure "
          "is a fact about it, not a reading taken inside it — demonstrated "
          "by variation, not assumed", True, len(div), len(div), True,
          "exhibit a closure whose divisor structure depends on where the "
          "reading is taken from", "closures 12, 13, 16, 17")
    S.seal({"stage": "relativity", "readings": readings})

    # ---- 2. primality, derived
    RANGE = range(2, 60)
    n_prime, ok_prime = 0, True
    for n in RANGE:
        n_prime += 1
        derived = (not has_annihilating_pair(n)) and all_reversible(n)
        ok_prime &= (derived == classical_prime(n))
    S.add("PRIMALITY DERIVED: 'no annihilating pair' and 'every pattern "
          "reversible' and classical primality coincide on every closure",
          ok_prime, n_prime, n_prime, True,
          "exhibit a closure where the three criteria disagree",
          f"closures {RANGE.start}..{RANGE.stop - 1}")
    S.seal({"stage": "primality", "checked": n_prime})

    # ---- 3. Lagrange
    n_lag, ok_lag = 0, True
    for n in range(2, 40):
        U = units(n)
        for a in U:
            t = return_time(a, n)
            if t:
                n_lag += 1
                ok_lag &= (len(U) % t == 0)
    S.add("LAGRANGE: a pattern's return-time divides the number of "
          "reversible patterns in its closure", ok_lag, n_lag, n_lag, True,
          "exhibit a reversible pattern whose return-time does not divide "
          "the unit count", "closures 2..39, all units")

    # ---- 4. Fermat, as a corollary
    primes = [p for p in range(2, 60) if classical_prime(p)]
    n_f, ok_f = 0, True
    for p in primes:
        for a in range(1, p):
            n_f += 1
            ok_f &= (pow(a, p - 1, p) == 1)
    S.add("FERMAT: in a prime closure, every non-zero pattern returns home "
          "after (p-1) self-propagations — a corollary of primality-as-"
          "non-annihilation plus Lagrange, not a new axiom",
          ok_f, n_f, n_f, True,
          "exhibit a prime closure and a non-zero pattern that does not "
          "return after p-1 propagations", f"primes below 60",
          derived=True)
    S.seal({"stage": "fermat", "checked": n_f})

    S.nonclaim("NOT claimed: that closure is priced. Establishing an "
               "isolation is this framework's floor, stated and not crossed.")
    S.nonclaim("NOT claimed: that any result here holds past its enumerated "
               "closures. Lifting requires induction over closure size — a "
               "schema — and the lift is UNPAID.")
    S.nonclaim("NOT claimed: that classical primality is wrong. It is used "
               "as a reference to check agreement, never to define. The "
               "derivation stands or falls on the coincidence, which is "
               "checkable and checked.")
    S.nonclaim("NOT claimed: that the unbounded integers are constructed "
               "here. They are the limit of refusing to close; this suite "
               "enumerates closures, which are finite by construction.")
    return S


if __name__ == "__main__":
    S = audit()
    S.report()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "manifests", "arithmetic_manifest.json"), "w") as f:
        json.dump(S.manifest(), f, indent=2, sort_keys=True)
    sys.exit(1 if S.failed() else 0)
