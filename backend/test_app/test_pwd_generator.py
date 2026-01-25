import pytest
from pwd_generator.pwd_generator import (
    generate_password,
    create_password,
)


@pytest.fixture
def test_symbols():
    return "~!@#$%^&*()-_+=,.?:;"


@pytest.fixture
def test_numbers():
    return "1234567890"


@pytest.fixture
def test_mixed_case():
    return "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"


@pytest.fixture
def test_single_case():
    return "qwertyuiopasdfghjklzxcvbnm"


def count_characters(pwd, test_symbols):
    """
    counter helper
    """
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


def test_create_password_01(test_symbols, test_numbers, test_mixed_case):
    """
    length = 0
    """
    pwd = create_password(
        0, test_symbols, test_numbers, test_mixed_case,
        0, 0, 0,
    )

    assert len(pwd) == 0


def test_create_password_02(test_symbols, test_numbers, test_mixed_case):
    """
    length = 16
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_mixed_case,
        1, 1, 14,
    )

    assert len(pwd) == 16


def test_create_password_03(test_symbols, test_numbers, test_mixed_case):
    """
    4 symbols, 4 digits, 8 letters
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_mixed_case,
        4, 4, 8,
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 4
    assert numbers == 4
    assert letters == 8


def test_create_password_04(test_symbols, test_mixed_case):
    """
    no digits
    """
    pwd = create_password(
        16, test_symbols, "", test_mixed_case,
        4, 0, 12,
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 4
    assert numbers == 0
    assert letters == 12


def test_create_password_05(test_symbols, test_numbers, test_mixed_case):
    """
    no symbols
    """
    pwd = create_password(
        16, "", test_numbers, test_mixed_case,
        0, 2, 14,
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 0
    assert numbers == 2
    assert letters == 14


def test_create_password_06(test_symbols, test_numbers, test_single_case):
    """
    no upper case
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_single_case,
        1, 3, 12,
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)

    assert len(pwd) == 16
    assert uppers == 0
    assert symbols == 1
    assert numbers == 3
    assert lowers == 12


def test_generate_pwd_01(test_symbols):
    """
    All flags set (default args)
    """
    pwd = generate_password()

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols + numbers + letters == len(pwd)
    assert symbols >= 1
    assert symbols <= 4
    assert numbers >= 1
    assert numbers <= 4
    assert letters == (16 - symbols - numbers)


def test_generate_pwd_02(test_symbols):
    """
    No digits, length = 12
    """
    pwd = generate_password(
        length=12,
        has_numbers=False,
    )

    N = len(pwd)
    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert N == 12
    assert symbols + numbers + letters == N
    assert symbols > 0
    assert symbols <= (N // 4)
    assert numbers == 0
    assert letters == (N - symbols - numbers)


def test_generate_pwd_03(test_symbols):
    """
    No flags set
    """
    pwd = generate_password(
        length=20,
        has_symbols=False,
        has_numbers=False,
        mixed_case=False
    )

    N = len(pwd)
    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert N == 20
    assert symbols + numbers + letters == N
    assert symbols == 0
    assert numbers == 0
    assert uppers == 0
    assert letters == (N - symbols - numbers)


def test_generate_pwd_04(test_symbols):
    """
    flags set, large length
    """
    pwd = generate_password(length=63)
    N = len(pwd)
    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert N == 63
    assert symbols + numbers + letters == N
    assert symbols > 0
    assert symbols <= (N // 4)
    assert numbers > 0
    assert numbers <= (N // 4)
    assert letters == (N - symbols - numbers)
