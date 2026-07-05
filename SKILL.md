---
name: council
description: >-
  Convene a blind, evidence-first council on an important decision. Independent
  seats argue in parallel (none sees another), critique each other once while
  anonymized, and a chair synthesizes a verdict by evidence tier -- not by vote
  count or eloquence. Use for spec approvals, gate pass/fail calls, irreversible
  operations (deletes, migrations, history rewrites), "is this claim actually
  true" disputes, and any decision where the proposer or orchestrator has a
  visible preferred answer. The council RECOMMENDS; the user RATIFIES. Do NOT use
  for routine execution, trivia, or anything a single run / test / query settles
  directly.
---

# Council

The council is the BOARD: independent oversight that recommends but does not
execute. It exists to catch what a single confident pass misses -- unstated
assumptions, unchecked numbers, same-DNA blind spots, second-order effects, and
the question nobody thought to ask. A good board, not a rubber stamp: evidence
over eloquence, no forced-dissent quotas, and a panel sized to the stakes.

The mechanics that must be exact (panel selection, blind anonymization, the
verdict scaffold) live in a deterministic helper so they never drift. The
JUDGMENT is the council's; the helper only handles bookkeeping.

## Before acting

1. READ `references/roster.md` -- the 8 seats and the ARGUMENT RUBRIC every seat
   must produce (this is the "beef": the structured case, not a vibe).
2. READ `references/flow.md` -- the 5-phase protocol (FRAME, SELECT, ROUND 1,
   ROUND 2, CHAIR) and the verdict scaffold sections.
3. COMPUTE `SKILL_DIR` = the directory THIS SKILL.md lives in. Every helper call
   below is `python "<SKILL_DIR>/scripts/council.py" ...`. Never hardcode a path.
4. VERIFY the helper responds:
   `python "<SKILL_DIR>/scripts/council.py" select-panel --weight standard`
   It should print a JSON seat list. If it errors, stop and fix before convening.

## The 5-phase flow in brief

See `references/flow.md` for each phase in full. In short:

1. FRAME -- restate the decision NEUTRALLY. Strip the proposer's lean and your
   own. One sentence a skeptic and an advocate would both accept as fair.

2. SELECT -- pick the panel by blast radius, not by feel:
   `python "<SKILL_DIR>/scripts/council.py" select-panel --weight <routine|standard|heavy|irreversible>`
   The helper returns the seats. INVARIANT: ADVOCATE and RED_TEAM are always
   paired (a steelman is only honest when its adversary argues at full strength).

3. ROUND 1 (blind, parallel) -- spawn the selected seats IN ONE MESSAGE so none
   sees another's output. Each returns a rubric-structured argument from
   `references/roster.md`: Position -> tagged Claims -> Warrant -> anticipated
   counter -> Confidence (0-1) -> Falsifier.

4. ROUND 2 (one rebuttal) -- anonymize the Round 1 outputs (present peers as
   Response A/B/C via the helper's blind protocol) and show each seat the others.
   Each CONCEDES what it must, HOLDS what survives, and gives its strongest
   COUNTER to the strongest opposing claim. Exactly one rebuttal round.

5. CHAIR -- synthesize by EVIDENCE TIER (PRIMARY > DERIVED > ASSERTED), never by
   vote or eloquence. Run a completeness sweep (what is MISSING: unasked
   question, ungathered evidence, unconsidered option). Emit the scaffold:
   `python "<SKILL_DIR>/scripts/council.py" verdict-scaffold --question "<neutral frame>" --weight <weight>`
   Fill every section. The USER is the final ratifier: the council recommends,
   the user decides.

## Cross-vendor seat

If the `irreversible` panel is selected it includes CROSS_VENDOR -- a seat meant
to run on a DIFFERENT model family to break same-DNA bias. If you have a
second-vendor CLI available (a different model family), wire that one seat
through it. If you do not, run the seat in-model but note "single-vendor council"
in the verdict so the reader knows the same-DNA check was not truly independent.
