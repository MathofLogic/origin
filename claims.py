"""
Shared claim machinery. The tier is NOT a label — it is the coverage ratio
of the verification against the scope the claim ranges over. Nothing that
uses this module can assert a tier; it can only report what it discharged.

No claim exists without a falsifier. That is enforced at construction.
"""
from fractions import Fraction as F
import hashlib, json

ORDER = ["FORCED", "FORCED-on-cut", "EMPIRICAL", "CONDITIONAL",
         "PRESUMED", "STIPULATED", "UNPAID"]


def tier(discharged, scope, scope_declared, derived=False):
    """discharged : distinctions actually checked
       scope      : distinctions the claim ranges over (None = unbounded)
       scope_declared : is the scope stated as PART OF the claim?"""
    if scope in (None, 0):
        return "CONDITIONAL" if derived else "UNPAID"
    r = F(discharged, scope)
    if r == 1:
        return "FORCED-on-cut" if scope_declared else "FORCED"
    if r > 0:
        return "EMPIRICAL"
    return "CONDITIONAL" if derived else "UNPAID"


class Claim:
    __slots__ = ("text", "held", "n", "scope", "declared", "falsifier",
                 "cut", "derived", "tier")

    def __init__(self, text, held, discharged, scope, declared,
                 falsifier, cut="", derived=False):
        if not falsifier:
            raise ValueError(f"claim has no falsifier: {text}")
        self.text, self.held, self.n = text, bool(held), discharged
        self.scope, self.declared, self.cut = scope, declared, cut
        self.falsifier, self.derived = falsifier, derived
        self.tier = tier(discharged, scope, declared, derived) if held \
            else "UNPAID"

    def row(self):
        return {"claim": self.text, "held": self.held, "tier": self.tier,
                "discharged": self.n, "scope": self.scope, "cut": self.cut,
                "falsifier": self.falsifier}


class Suite:
    def __init__(self, name, source_path):
        self.name, self.src = name, source_path
        self.claims, self.nonclaims, self.chain = [], [], []

    def add(self, *a, **k):
        c = Claim(*a, **k); self.claims.append(c); return c

    def nonclaim(self, t): self.nonclaims.append(t)

    def seal(self, obj):
        prev = self.chain[-1] if self.chain else "genesis"
        blob = json.dumps(obj, sort_keys=True, default=str) + prev
        self.chain.append(hashlib.sha256(blob.encode()).hexdigest()[:16])
        return self.chain[-1]

    def sha(self):
        return hashlib.sha256(open(self.src, "rb").read()).hexdigest()[:16]

    def verdict(self):
        if not self.claims:
            return "UNPAID"
        return ORDER[max(ORDER.index(c.tier) for c in self.claims)]

    def failed(self):
        return [c for c in self.claims if not c.held]

    def manifest(self):
        """Deterministic. No timestamps — must regenerate byte-identical."""
        return {
            "suite": self.name,
            "source_sha256_16": self.sha(),
            "claims": [c.row() for c in self.claims],
            "nonclaims": self.nonclaims,
            "chain": self.chain,
            "verdict": self.verdict(),
            "claims_without_falsifier": 0,
        }

    def report(self):
        print("=" * 70)
        print(f"  {self.name}")
        print("=" * 70)
        for c in self.claims:
            mark = "PASS" if c.held else "FAIL"
            print(f"  [{c.tier:<13}][{mark}] {c.text}")
            print(f"      discharged {c.n:,} / scope "
                  f"{c.scope if c.scope is not None else 'unbounded'}"
                  + (f"   cut: {c.cut}" if c.cut else ""))
            print(f"      falsifier: {c.falsifier}")
        if self.nonclaims:
            print("\n  NON-CLAIMS")
            for n in self.nonclaims:
                print(f"    - {n}")
        counts = {}
        for c in self.claims:
            counts[c.tier] = counts.get(c.tier, 0) + 1
        print("\n" + "-" * 70)
        print("  " + "   ".join(f"{t}:{counts[t]}" for t in ORDER if t in counts))
        print(f"  chain {len(self.chain)}   sha256[:16] = {self.sha()}")
        print(f"  verdict {'PASS' if not self.failed() else 'FAIL'}"
              f"/{self.verdict()}")
        print("-" * 70)
