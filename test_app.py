from app import get_max

def test_max_value():
    assert get_max(10, 5) == 10
    assert get_max(-1, -5) == -1
    assert get_max(0, 0) == 0
    assert get_max(3.5, 2.8) == 3.5