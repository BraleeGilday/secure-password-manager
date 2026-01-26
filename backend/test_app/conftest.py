import pytest


@pytest.fixture()
def test_symbols():
    return "~!@#$%^&*()-_+=,.?:;"


@pytest.fixture()
def count_characters(test_symbols):
    """
    counter helper (move to conftest.py?)
    """
    def _count(pwd):
        symbols = 0
        numbers = 0
        lowers = 0
        uppers = 0

        for c in pwd:
            if c in test_symbols:
                symbols += 1
            elif c.isdigit():
                numbers += 1
            elif c.islower():
                lowers += 1
            elif c.isupper():
                uppers += 1

        return symbols, numbers, lowers, uppers
    return _count
