import council


def test_select_panel_scales_with_weight():
    assert council.select_panel("routine") == ["ANALYST", "CONTRARIAN", "EMPIRICIST"]
    assert len(council.select_panel("irreversible")) == 8
    assert "CROSS_VENDOR" in council.select_panel("irreversible")
    assert "CROSS_VENDOR" not in council.select_panel("routine")


# --- #2: an invalid weight is an error, never a smaller panel -----------------

import json
import subprocess
import sys
from pathlib import Path

import pytest

_CLI = Path(__file__).resolve().parent / "council.py"


@pytest.mark.parametrize("bad", ["whatever", "irreversable", "heavvy", "", "  ", None, 3,
                                 "standard panel", "routine,heavy"])
def test_unknown_weight_is_rejected(bad):
    with pytest.raises(ValueError) as e:
        council.select_panel(bad)
    for w in council.VALID_WEIGHTS:          # the error teaches the valid values
        assert w in str(e.value)


@pytest.mark.parametrize("raw,canon", [("Heavy", "heavy"), ("  irreversible\n", "irreversible"),
                                       ("ROUTINE", "routine"), ("standard", "standard")])
def test_case_and_whitespace_are_forgiven(raw, canon):
    assert council.select_panel(raw) == council.PANELS[canon]


@pytest.mark.parametrize("cmd", [["select-panel"], ["verdict-scaffold", "--question", "q"]])
def test_cli_exits_nonzero_and_lists_valid_weights(cmd):
    r = subprocess.run([sys.executable, str(_CLI), *cmd, "--weight", "irreversable"],
                       capture_output=True, text=True)
    assert r.returncode == 2
    assert r.stdout == ""                                   # no panel printed
    assert "irreversable" in r.stderr
    assert all(w in r.stderr for w in council.VALID_WEIGHTS)


def test_cli_accepts_a_valid_weight():
    r = subprocess.run([sys.executable, str(_CLI), "select-panel", "--weight", " Irreversible "],
                       capture_output=True, text=True, check=True)
    assert len(json.loads(r.stdout)) == 8


def test_advocate_and_redteam_are_always_paired():
    # a steelman is only honest when its adversary argues too
    for weight, seats in council.PANELS.items():
        assert ("ADVOCATE" in seats) == ("RED_TEAM" in seats), weight


def test_anonymize_is_blind_reversible_and_complete():
    outs = ["alpha", "bravo", "charlie", "delta"]
    anon, mapping = council.anonymize(outs, seed=0)
    assert sorted(x["label"] for x in anon) == ["A", "B", "C", "D"]   # relabeled A..D
    assert sorted(x["text"] for x in anon) == sorted(outs)            # nothing lost/dup'd
    for x in anon:                                                    # mapping de-anonymizes
        assert outs[mapping[x["label"]]] == x["text"]
    anon2, _ = council.anonymize(outs, seed=0)                        # seed -> deterministic
    assert [x["text"] for x in anon2] == [x["text"] for x in anon]


def test_anonymize_actually_shuffles():
    outs = [str(i) for i in range(8)]
    orders = {tuple(x["text"] for x in council.anonymize(outs, seed=s)[0]) for s in range(5)}
    assert len(orders) > 1  # different seeds produce different orderings -> it shuffles


def test_verdict_scaffold_has_required_sections():
    s = council.verdict_scaffold("Ship it?", council.select_panel("heavy"))
    for section in ["VERDICT", "CONFIDENCE", "EVIDENCE INDEX", "FALSIFIERS", "DISSENT"]:
        assert section in s
    assert "Ship it?" in s
    assert "ADVOCATE" in s and "RED_TEAM" in s  # heavy panel seats are listed
