"""council.py -- deterministic helper for the /council skill.

Stdlib-only (portable). Owns the mechanics that must be exact rather than
prose-follows-vibes: panel selection by decision weight, blind anonymization
for the peer-review round, and the chairman's verdict scaffold. The JUDGMENT
is the council's; this file only handles the bookkeeping.

CLI: python council.py <select-panel|verdict-scaffold> ...
"""
import json
import random
import argparse

# The full roster. Seats are SELECTED from this per decision, never all-always.
ROSTER = [
    "ANALYST",       # close read; unstated assumptions; does the artifact say what is claimed
    "CONTRARIAN",    # find >=1 concrete flaw, or state none + what was checked
    "EMPIRICIST",    # re-derive every quantitative claim from primary sources
    "ADVOCATE",      # steelman: build the STRONGEST case FOR
    "RED_TEAM",      # adversary: assume it is wrong; full attack + 2nd-order effects
    "HISTORIAN",     # precedent: tried/decided before? repeats a known failure?
    "PRAGMATIST",    # cost/benefit: even if correct, is it worth it?
    "CROSS_VENDOR",  # a seat on a different model family; breaks same-DNA bias
]

# Panels scale to blast radius. INVARIANT: ADVOCATE and RED_TEAM are always
# paired -- a steelman is only honest when its adversary argues at full strength.
PANELS = {
    "routine":      ["ANALYST", "CONTRARIAN", "EMPIRICIST"],
    "standard":     ["ANALYST", "CONTRARIAN", "EMPIRICIST", "HISTORIAN"],
    "heavy":        ["ANALYST", "CONTRARIAN", "EMPIRICIST", "ADVOCATE", "RED_TEAM", "PRAGMATIST"],
    "irreversible": ["ANALYST", "CONTRARIAN", "EMPIRICIST", "ADVOCATE", "RED_TEAM",
                     "HISTORIAN", "PRAGMATIST", "CROSS_VENDOR"],
}


def select_panel(weight):
    """Return the seat list for a decision weight. Unknown weight -> 'standard'."""
    return list(PANELS.get(str(weight).lower(), PANELS["standard"]))


def anonymize(outputs, seed=None):
    """Shuffle + relabel seat outputs 'A','B','C',... for the blind peer round.

    Returns (anon_list, mapping): anon_list is [{'label','text'}, ...] in shuffled
    order; mapping[label] = original index, so the chair can de-anonymize after.
    """
    items = list(enumerate(list(outputs)))
    random.Random(seed).shuffle(items)
    anon, mapping = [], {}
    for i, (orig_idx, text) in enumerate(items):
        label = chr(ord("A") + i)
        anon.append({"label": label, "text": text})
        mapping[label] = orig_idx
    return anon, mapping


VERDICT_SECTIONS = [
    "VERDICT",
    "CONFIDENCE",
    "WHERE THE COUNCIL AGREED / CLASHED",
    "BLIND SPOTS (these become TODOs)",
    "DISSENT WORTH PRESERVING",
    "EVIDENCE INDEX (every file:line / query / command the verdict rests on)",
    "FALSIFIERS (what would overturn this verdict)",
    "SEATS (count, roles, blind protocol confirmed y/n)",
]


def verdict_scaffold(question, seats):
    """Return the chairman's verdict template -- the sections synthesis must fill."""
    lines = [f"## COUNCIL VERDICT: {question}", ""]
    for s in VERDICT_SECTIONS:
        lines.append(f"### {s}")
        lines.append("")
    lines.append(f"Seats convened ({len(seats)}): {', '.join(seats)}")
    return "\n".join(lines)


def _main():
    p = argparse.ArgumentParser(prog="council")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("select-panel")
    sp.add_argument("--weight", required=True,
                    help="routine | standard | heavy | irreversible")

    vs = sub.add_parser("verdict-scaffold")
    vs.add_argument("--question", required=True)
    vs.add_argument("--weight", required=True)

    a = p.parse_args()
    if a.cmd == "select-panel":
        print(json.dumps(select_panel(a.weight)))
    elif a.cmd == "verdict-scaffold":
        print(verdict_scaffold(a.question, select_panel(a.weight)))


if __name__ == "__main__":
    _main()
