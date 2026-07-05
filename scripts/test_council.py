import council


def test_select_panel_scales_with_weight():
    assert council.select_panel("routine") == ["ANALYST", "CONTRARIAN", "EMPIRICIST"]
    assert len(council.select_panel("irreversible")) == 8
    assert "CROSS_VENDOR" in council.select_panel("irreversible")
    assert "CROSS_VENDOR" not in council.select_panel("routine")
    # unknown weight falls back to 'standard'
    assert council.select_panel("whatever") == council.select_panel("standard")


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
