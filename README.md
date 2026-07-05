# Council

A blind, multi-seat review board for the decisions that are expensive to get
wrong. The Council does not execute anything. It convenes a panel of independent
minds, has them argue from evidence, and returns a single reasoned verdict. The
weight of that verdict is set by the strength of the argument behind it, not by
the count of hands raised.

> **Pairs with [Bob](https://github.com/Zuxas/bob), the foreman.** Bob does the
> work and consults this board at his gates; the Council reviews and recommends;
> you ratify.

## What the Council is: the BOARD

Think of a company.

- The **Council is the board of directors.** Independent oversight. It reviews,
  it challenges, it recommends. It never runs operations.
- **Bob is the foreman.** Bob does the work -- builds the thing, ships the
  change, runs the migration -- and stops at his gates to consult the board
  before anything irreversible.
- **You are the owner.** The board recommends; the foreman executes; the owner
  ratifies. The final call is always yours.

A good board is not a rubber stamp. It weighs evidence over eloquence, it does
not fill a quota of manufactured dissent, and it sizes its own attention to what
is actually at stake. That is the standard this Council is built to.

Council pairs with the **Bob** skill: Bob is the executor who consults this board
at his decision gates. Council is useful on its own for any high-stakes call, and
the two together give you an execute-and-review loop with the owner ratifying.

## How it works

### The roster: eight seats, selected -- never all-always

The full bench is eight independent seats. A panel is drawn from them per
decision, sized to the blast radius. No seat is seated by default; each is there
because the decision earned it.

- **ANALYST** -- close read. Surfaces unstated assumptions. Asks whether the
  artifact actually says what is claimed of it.
- **CONTRARIAN** -- finds at least one concrete flaw, or states plainly that it
  found none and names exactly what it checked.
- **EMPIRICIST** -- re-derives every quantitative claim from primary sources.
- **CROSS_VENDOR** -- a seat run on a different model family, to break same-DNA
  bias among the other seats.
- **ADVOCATE** -- the steelman. Builds the strongest possible case *for* the
  proposal.
- **RED_TEAM** -- the adversary. Assumes the proposal is wrong and mounts a full
  attack, including second-order effects and the worst case.
- **HISTORIAN** -- precedent. Has this been tried or decided before? Does it
  repeat a known failure or contradict a past verdict?
- **PRAGMATIST** -- cost and benefit. Even if it is correct, is it worth it?
  Weighs opportunity cost, maintenance, and simpler alternatives.

**Invariant: ADVOCATE and RED_TEAM are always paired.** A steelman is only
honest when its adversary is arguing at full strength; neither is seated without
the other.

Panels scale to blast radius:

- **routine** -- ANALYST, CONTRARIAN, EMPIRICIST
- **standard** -- adds HISTORIAN
- **heavy** -- ANALYST, CONTRARIAN, EMPIRICIST, plus the ADVOCATE/RED_TEAM pair
  and PRAGMATIST
- **irreversible** -- the full bench of eight, including CROSS_VENDOR

### The argument rubric: the beef every seat must bring

An opinion is not evidence. Every seat returns a structured argument, not a
verdict-by-assertion:

- **Position**, then each **Claim** tagged by evidence tier:
  - **[PRIMARY]** -- cites a file and line, a command, or a query.
  - **[DERIVED]** -- reasoned from primary evidence.
  - **[ASSERTED]** -- stated without backing, and flagged as such.
- **Warrant** -- why the cited evidence actually supports the claim.
- The strongest **counter** the seat can anticipate against its own position.
- A calibrated **confidence** from 0 to 1.
- A **falsifier** -- the specific evidence that would flip the seat's verdict.

The tier tags are what let the chair weigh a well-cited claim above a
well-phrased one.

### The five phases

1. **FRAME** -- state the decision neutrally. Strip the proposer's lean and the
   chair's own.
2. **SELECT** -- pick the panel by blast radius (see the command below).
3. **ROUND 1** -- spawn every seat in one message: blind and parallel, no seat
   sees another's work. Each returns a rubric-structured argument.
4. **ROUND 2** -- one rebuttal round. Peers are anonymized and shown to each seat
   as Response A, B, C. Each seat concedes what it must, holds what survives, and
   gives its strongest counter to the strongest opposing claim.
5. **CHAIR** -- synthesize by evidence tier, not by vote count and not by
   eloquence. Run a completeness sweep for what is missing -- the unasked
   question, the ungathered evidence, the unconsidered option -- then emit the
   verdict.

The chair does not tally. It reads the arguments, weighs them by the tier of
evidence they rest on, and reports where the panel agreed, where it clashed, and
what dissent is worth preserving. The user is the final ratifier.

## Why it's useful

- **It catches confident-but-wrong before it ships.** The EMPIRICIST re-derives
  numbers from source; the RED_TEAM assumes the thing is broken and looks for
  how. A claim that reads clean can still fail both, and the panel is built to
  make that visible before it costs you.
- **Independence is structural, not requested.** Round 1 is blind and parallel,
  so no seat anchors on another. The CROSS_VENDOR seat runs on a different model
  family, so the panel does not share one lineage's blind spots.
- **It is a good board, not a rubber stamp.** Evidence outranks eloquence.
  There are no forced-dissent quotas -- a seat that finds nothing says so and
  names what it checked. And the panel is sized to the stakes, so a routine call
  does not summon the full bench and an irreversible one is not waved through
  thin.

## Bring your own second opinion

One seat stands apart: **CROSS_VENDOR** runs on a *different model family* than the
rest of the board. It is the panel's guard against sharing one lineage's blind
spots -- a second set of eyes with different training DNA, which is often exactly
where the sharpest catch comes from.

It is optional, but take it if you can. If you have another agent off-platform --
a different model's CLI, your own tooling, anything that reads a prompt and returns
an argument -- you are invited to seat it as the cross-vendor chair. Just point to
it in your `.council-convention.md`:

```text
# cross-vendor-cmd: <your-second-vendor-cli> <args>
```

No second vendor on hand? No problem. The board seats the rest of the roster and
notes the cross-vendor chair sat empty -- your verdict is still sound, just
single-lineage. But if you have one, it is the cheapest upgrade in the building.

## How to use it

Three moves, and the last one is always yours.

**1 &mdash; Frame the decision as one neutral question.** Strip your own lean out of
it: *"Should we ship X?"*, not *"X is ready, right?"* A leading question hands you
the answer you wanted, not the one you needed.

**2 &mdash; Convene the board** with that question, and point it at something
concrete to weigh &mdash; a spec, a diff, a dataset, the claim in dispute. Judgment
needs an artifact, not a vibe:

```text
/council "your decision, stated as one neutral question"
```

**3 &mdash; Size the panel to the stakes.** Heavier decisions seat more of the bench:

| Weight | Seats it convenes | Use for |
| --- | --- | --- |
| `routine` | Analyst, Contrarian, Empiricist | low-blast-radius calls |
| `standard` | &nbsp;&nbsp;+ Historian | the everyday default |
| `heavy` | &nbsp;&nbsp;+ the Advocate / Red-team pair, Pragmatist | expensive to reverse |
| `irreversible` | the full bench of eight, incl. Cross-vendor | deletes, migrations, history rewrites |

```text
python scripts/council.py select-panel --weight heavy
python scripts/council.py verdict-scaffold --question "<your question>" --weight heavy
```

(`council.py` only handles the mechanics that must stay exact &mdash; who sits, the
blind shuffle for the rebuttal round, and the verdict template. The judgment is the
board's.)

Then the verdict comes back &mdash; and it is a **recommendation**, not an order.
The board convenes the minds and reports what the evidence supports; **you ratify.**
The board recommends; the owner decides.

## Tuning the Council

Every knob lives in one of two places -- the convention file (no code) or the
small helper (for tinkerers):

- **`.council-convention.md`** (copy it from `CONVENTION-TEMPLATE.md`) is the
  front panel: your default panel weight, extra domain seats, your cross-vendor
  CLI command, and where verdicts get filed. Edit it -- no code needed.
- **`scripts/council.py`** holds the deeper knobs: the `PANELS` map (which seats
  each weight convenes) and the `ROSTER` itself. Change these for a different
  bench or different panel sizing. The tests pin the invariants (Advocate and
  Red-team stay paired), so run `pytest` after you tweak.

The Council recommends; you ratify. No knob changes that.

## Install

Clone into your skills directory:

```text
# Global -- available in every project:
git clone https://github.com/Zuxas/council.git ~/.claude/skills/council

# Or per-project, from that repo's root:
git clone https://github.com/Zuxas/council.git .claude/skills/council
```

Requirements: Python (standard library only -- no third-party packages).

Verify the deterministic helper from the scripts directory:

```text
cd ~/.claude/skills/council/scripts && pytest
```

## Credits

Built on the blind-panel / LLM-as-judge lineage, with a nod to **Matt Pocock**
([@mattpocock](https://github.com/mattpocock)). Tweaked for my own use -- take it
and make it yours if it helps. :]

Pairs with **[Bob](https://github.com/Zuxas/bob)**.
