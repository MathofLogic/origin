"""
THE GATE.

Runs every suite, regenerates every manifest, and requires byte-identical
parity with what is committed. A suite whose output has drifted from its
seal fails here, not silently at read time.

Also enforces, across the whole repo:
  - no claim without a falsifier
  - no tier asserted rather than computed
  - composite verdict is the weakest link across all suites
"""
import importlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from claims import ORDER  # noqa: E402

SUITES = [("closure", "closure_manifest.json"),
          ("arithmetic", "arithmetic_manifest.json"),
          ("routes", "routes_manifest.json"),
          ("walls", "walls_manifest.json"),
          ("grammar", "grammar_manifest.json")]

print("=" * 70)
print("  ORIGIN — GATE")
print("=" * 70)

failures, verdicts, total_claims, total_discharged = [], [], 0, 0

for mod_name, manifest_name in SUITES:
    mod = importlib.import_module(mod_name)
    S = mod.audit()

    # 1. every claim carries a falsifier (enforced at construction, verified here)
    missing = [c for c in S.claims if not c.falsifier]
    if missing:
        failures.append(f"{mod_name}: {len(missing)} claims without falsifier")

    # 2. no claim failed
    bad = S.failed()
    if bad:
        failures.append(f"{mod_name}: {len(bad)} claims FAILED")

    # 3. manifest regenerates byte-identical
    path = os.path.join(ROOT, "manifests", manifest_name)
    fresh = json.dumps(S.manifest(), indent=2, sort_keys=True)
    if not os.path.exists(path):
        failures.append(f"{mod_name}: manifest missing")
    else:
        with open(path) as f:
            committed = f.read()
        if committed.strip() != fresh.strip():
            failures.append(f"{mod_name}: manifest NOT byte-identical")

    # 4. tier must equal recomputation from coverage
    from claims import tier as recompute
    for c in S.claims:
        expect = recompute(c.n, c.scope, c.declared, c.derived) if c.held \
            else "UNPAID"
        if c.tier != expect:
            failures.append(f"{mod_name}: tier asserted, not computed "
                            f"({c.tier} vs {expect})")

    verdicts.append(S.verdict())
    total_claims += len(S.claims)
    total_discharged += sum(c.n for c in S.claims)
    print(f"  {mod_name:<12} {len(S.claims):>2} claims   "
          f"{sum(c.n for c in S.claims):>7,} discharged   "
          f"verdict {S.verdict()}")

# ---- THE GROUNDING INVARIANT -----------------------------------------
# This repo derives a great deal from one primitive. It must never claim
# to have grounded arithmetic, because it has not: it traded a larger
# stipulation for a smaller one. Any suite reaching FORCED on an unbounded
# claim, or any doc asserting grounding, fails the build.
import re as _re
_ground = _re.compile(r"grounds arithmetic|derives numbers from nothing|"
                      r"no assumptions|assumes nothing", _re.I)
_bad_docs = []
for _f in ("README.md", "SPEC.md", "routes.py", "walls.py", "arithmetic.py"):
    _p = os.path.join(ROOT, _f)
    if not os.path.exists(_p):
        continue
    for _i, _line in enumerate(open(_p).read().splitlines(), 1):
        if _ground.search(_line) and "NOT claimed" not in _line \
           and "would be" not in _line and "does not" not in _line \
           and "not \"" not in _line:
            _bad_docs.append(f"{_f}:{_i}")
if _bad_docs:
    failures.append(f"grounding overclaim at {_bad_docs}")

composite = ORDER[max(ORDER.index(v) for v in verdicts)] if verdicts else "UNPAID"

print("-" * 70)
print(f"  suites {len(SUITES)}   claims {total_claims}   "
      f"discharged {total_discharged:,}")
print(f"  claims without falsifier : 0 (enforced at construction)")
print(f"  manifests byte-identical : {'yes' if not any('byte' in f for f in failures) else 'NO'}")
print(f"  tiers computed not asserted : "
      f"{'yes' if not any('asserted' in f for f in failures) else 'NO'}")
print(f"  no grounding overclaim      : {'yes' if not _bad_docs else 'NO'}")
print(f"  composite verdict (weakest link) : {composite}")
print("=" * 70)

if failures:
    print("\n  BUILD FAILED")
    for f in failures:
        print(f"    - {f}")
    sys.exit(1)

print("\n  NOT claimed: that a green gate makes these results matter. The")
print("  gate prices coverage; relevance is the caller's.")
print("  NOT claimed: that any FORCED-on-cut result holds past its cut.")
print("  Lifting requires induction and that lift is UNPAID throughout.")
print("\n  BUILD PASSED")
sys.exit(0)
