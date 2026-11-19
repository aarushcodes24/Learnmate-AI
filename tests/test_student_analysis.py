from app.ai.student_analysis import _bounded_score


def test_bounded_score():
    assert _bounded_score(120) == 100
    assert _bounded_score(-10) == 0
    assert _bounded_score("75") == 75
    assert _bounded_score("bad") == 0
