# origin

**Where numbers come from — two routes, and the wall they share.**

```
BUILD PASSED
suites 4   claims 20   composite verdict: CONDITIONAL
no grounding overclaim : yes
```

Stdlib only. Python 3.8+. Running any file **is** its audit.

---

## Two routes to the same arithmetic

**The axiomatic route.** Posit 0. Posit a successor. Define `+` and `×` by
recursion. Add induction to fix which structure you meant.

**The mechanism route.** Posit a pattern that returns to itself. Ask what it can
distinguish.

| object | axiomatic | mechanism |
|---|---|---|
| successor | posited | **derived** — co-propagation with the smallest non-loadless pattern |
| addition | defined by recursion | **derived** — two patterns propagated together |
| multiplication | defined by recursion | **derived** — one pattern propagated repeatedly |
| modular structure | constructed, then reduced | **is the closure**, directly |
| the integers | posited | the limit of *refusing* to close |
| primality | defined | **derived** — closures where no two non-trivial patterns wholly cancel |

`routes.py` checks that the two agree: successor over `{0..8}`, addition and
multiplication over all 81 pairs. They do.

---

## What each route had to assume

```
axiomatic route posits 7 things    mechanism route posits 1
```

Successor, addition and multiplication move from the posited column to the
derived column. **That is the result, and it is smaller than it sounds.**

A closure is a stipulation. Something had to be held apart well enough to return
to itself, and this repo does not price that. The mechanism route **trades a
larger assumption for a smaller one**. It does not escape assumption, and the
gate fails the build if any document claims it does.

---

## The wall both routes hit

Commutativity of addition holds for every pair checked. That is `FORCED-on-cut`,
not `FORCED` — the value space is unbounded and the check is finite.

Peano closes the gap with **induction**, which is a *schema*: one axiom per
predicate, infinitely many. No enumeration closes an infinite axiom family.

**The mechanism route has no better answer.** Deriving successor from a closure
moves the stipulation; it does not move the wall.

---

## Four walls, exhibited

`walls.py` runs each one rather than describing it.

| wall | what it shows |
|---|---|
| **1 — induction** | a finite cut cannot certify an unbounded claim |
| **1b — the intruder** | a structure satisfying the first four axioms that is *not* the naturals; only induction excludes it. This is what the schema buys, made visible |
| **2 — Gödel** | grounding from inside is unavailable; Gentzen's proof is a *trade* for a stronger assumption elsewhere, not a grounding |
| **3 — the closure** | the mechanism route's own floor, and the direct analogue of Wall 2 |

Wall 3 is the addition. Walls 1, 1b and 2 came from the axiomatic treatment and
apply to the mechanism route unchanged.

---

## On coinciding with standard mathematics

Several results here — Lagrange, Fermat, the ring laws — coincide with
established mathematics. **Arriving at established results by an independent
route is confirmation that the route works, not a discovery.** No priority is
claimed for any of them. What is claimed is the derivation *order*, and that is
checkable.

---

## Run it

```bash
python closure.py      # the primitive: group structure, multiplication
python arithmetic.py   # primality, Lagrange, Fermat from closure
python routes.py       # the two routes compared
python walls.py        # where both stop
python tests/run.py    # the gate
```
