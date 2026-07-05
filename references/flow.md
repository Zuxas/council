# Flow -- the 5-phase council protocol

The company metaphor holds throughout: the council is the BOARD (independent
oversight; recommends, does not execute), the foreman executes and consults the
board at his gates, and the user is the OWNER and final ratifier. The board's job
is a real recommendation grounded in evidence -- not a rubber stamp, and not a
forced quota of dissent.

All helper calls are `python "<SKILL_DIR>/scripts/council.py" ...`, where
SKILL_DIR is the directory the skill's SKILL.md lives in.

---

## Phase 1 -- FRAME

State the decision NEUTRALLY. Strip out the proposer's lean AND your own. The
frame is a single sentence that both a committed advocate and a committed skeptic
would accept as a fair statement of what is being decided.

- Remove loaded verbs ("finally fix", "obviously", "just").
- Name the actual choice and its alternatives, not a foregone conclusion.
- If you cannot write a frame both sides would sign, you do not yet understand
  the decision -- resolve that before selecting a panel.

Output: the neutral frame, quoted, so every downstream seat argues the same
question.

---

## Phase 2 -- SELECT

Pick the panel by BLAST RADIUS, not by feel. Weights:

- routine      -- low stakes, easily reversible, small surface.
- standard     -- normal decision with some downstream reach.
- heavy        -- significant commitment, hard to unwind, wide surface.
- irreversible -- deletes, migrations, history rewrites, anything you cannot take
                  back, or anything outward-facing / high-consequence.

Run:

    python "<SKILL_DIR>/scripts/council.py" select-panel --weight <weight>

The helper returns the seat list for that weight (see references/roster.md for
which seats each panel contains). Do not add or drop seats by hand -- the panel
map is the contract. INVARIANT enforced by the map: ADVOCATE and RED_TEAM appear
together or not at all.

---

## Phase 3 -- ROUND 1 (blind, parallel)

Spawn every selected seat IN ONE MESSAGE. This is what makes the round blind: no
seat sees any other seat's output, so there is no anchoring, no deference, no
bandwagon. Each seat argues the SAME neutral frame from Phase 1.

Each seat returns the full ARGUMENT RUBRIC from references/roster.md:
Position -> tagged Claims ([PRIMARY | DERIVED | ASSERTED]) -> Warrant per claim
-> Anticipated counter -> Confidence (0.0-1.0) -> Falsifier.

Do not summarize or reconcile yet. Collect all Round 1 arguments verbatim.

---

## Phase 4 -- ROUND 2 (one rebuttal, anonymized)

Exactly ONE rebuttal round. Anonymize the Round 1 outputs so seats judge
arguments, not authors: present each peer's argument as Response A, Response B,
Response C, ... The helper owns the blind relabel + the mapping back:

    (council.py's anonymize step shuffles and relabels the Round 1 outputs to
     A/B/C and keeps the label -> original-seat mapping for the chair.)

Show each seat all the OTHER seats' arguments (anonymized), never its own back to
it. Each seat then does exactly three things:

- CONCEDE -- name every point it now accepts and drop the claims that did not
  survive. Conceding is a strength, not a loss.
- HOLD -- restate the claims that SURVIVED contact with the others, and why they
  still stand.
- COUNTER -- give its single strongest rebuttal to the strongest OPPOSING claim
  in the anonymized set.

One round only. No further ping-pong; the chair takes it from here.

---

## Phase 5 -- CHAIR

The chair synthesizes -- by EVIDENCE TIER, never by vote count and never by
eloquence. A lone seat with a PRIMARY citation outranks a fluent majority resting
on ASSERTED claims.

Chair duties:

1. Rank the surviving claims: PRIMARY > DERIVED > ASSERTED. Resolve clashes on
   the evidence, not the head count.
2. COMPLETENESS SWEEP -- ask what is MISSING that no seat raised:
   - an unasked question,
   - evidence nobody gathered,
   - an option nobody considered.
   Missing items become TODOs in the verdict; they are first-class output.
3. Emit the verdict scaffold and fill every section:

    python "<SKILL_DIR>/scripts/council.py" verdict-scaffold --question "<neutral frame>" --weight <weight>

The USER is the final ratifier. The council RECOMMENDS; the user DECIDES. State
the recommendation plainly and hand the decision back.

---

## Verdict scaffold -- the sections the chair fills

The helper emits these; synthesis must fill each:

- VERDICT -- the recommendation, plus the calibrated CONFIDENCE.
- CONFIDENCE -- the chair's own 0.0-1.0, with a one-line why.
- WHERE THE COUNCIL AGREED / CLASHED -- consensus and the live disagreements,
  named honestly (do not launder a clash into false agreement).
- BLIND SPOTS (these become TODOs) -- the completeness-sweep findings: unasked
  questions, ungathered evidence, unconsidered options.
- DISSENT WORTH PRESERVING -- any minority position strong enough that the record
  should keep it, even though the verdict went the other way.
- EVIDENCE INDEX -- every file:line / query / command the verdict rests on, so a
  reader can re-check the primary basis without re-running the council.
- FALSIFIERS -- what specific evidence would OVERTURN this verdict.
- SEATS -- count, roles convened, and blind protocol confirmed (y/n). If the
  cross-vendor seat ran in-model, record "single-vendor council" here.
