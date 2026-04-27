from lcos.governance.decision import Decision


def test_decision_status_is_preserved() -> None:
    decision = Decision(status="HOLD", reason="insufficient evidence", confidence=0.4)
    assert decision.status == "HOLD"
    assert decision.confidence == 0.4
