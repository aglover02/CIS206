import builtins
import math
import bmi_app  

def test_happy_path_bmi_and_legend(capsys):
    bmi = bmi_app.calculate_bmi(150, 5, 7)  # 150 lb, 5'7"
    assert math.isclose(bmi, 23.4907551793, rel_tol=1e-6)
    bmi_app.display_bmi_and_legend(bmi)
    out = capsys.readouterr().out
    assert "Your BMI is: 23.5" in out
    assert "BMI Category Legend" in out
    assert "Underweight" in out and "Normal weight" in out and "Overweight" in out

def test_table_contains_expected_header_and_sample_value(capsys):
    bmi_app.display_bmi_table()
    out = capsys.readouterr().out
    # Header sanity
    assert "BMI Table" in out
    assert "58" in out and "60" in out and "76" in out
    # Sample known value: 100 lb @ 58 in -> ~20.9
    # It should appear as "  20.9" aligned in a column; use substring check:
    assert "20.9" in out

def test_zero_height_raises_value_error():
    try:
        bmi_app.calculate_bmi(150, 0, 0)
        assert False, "Expected ValueError for zero/invalid height"
    except ValueError as e:
        assert "greater than zero" in str(e)

def test_unrealistic_bmi_raises_assertion():
    # 600 lb, 3'0" → BMI ~325, triggers assertion
    try:
        bmi_app.calculate_bmi(600, 3, 0)
        assert False, "Expected AssertionError for unrealistic BMI"
    except AssertionError as e:
        assert "outside realistic human range" in str(e)

def test_quit_returns_none(monkeypatch):
    # Simulate entering 'q' at the first prompt
    inputs = iter(["q"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    result = bmi_app.get_user_input()
    assert result is None
