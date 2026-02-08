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
def test_uppers():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@pytest.fixture
def test_lowers():
    return "abcdefghijklmnopqrstuvwxyz"


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


def test_create_password_01(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    length = 0
    """
    pwd = create_password(
        0, test_symbols, test_numbers, test_lowers, test_uppers,
        0, 0, 0, 0
    )

    assert len(pwd) == 0


def test_create_password_01a(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    length = 0; passed int values
    """
    pwd = create_password(
        0, test_symbols, test_numbers, test_lowers, test_uppers,
        3, 3, 9, 1
    )

    assert len(pwd) == 0


def test_create_password_02(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    length = 16
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_lowers, test_uppers,
        1, 1, 7, 7
    )

    assert len(pwd) == 16


def test_create_password_03(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    4 symbols, 4 digits, 8 letters (6 + 2)
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_lowers, test_uppers,
        4, 4, 6, 2
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 4
    assert numbers == 4
    assert letters == 8


def test_create_password_04(test_symbols, test_lowers, test_uppers):
    """
    no digits
    """
    pwd = create_password(
        16, test_symbols, "", test_lowers, test_uppers,
        4, 0, 8, 4
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 4
    assert numbers == 0
    assert letters == 12


def test_create_password_05(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    no symbols
    """
    pwd = create_password(
        16, "", test_numbers, test_lowers, test_uppers,
        0, 2, 10, 4
    )

    symbols, numbers, lowers, uppers = count_characters(pwd, test_symbols)
    letters = lowers + uppers

    assert len(pwd) == 16
    assert symbols == 0
    assert numbers == 2
    assert letters == 14


def test_create_password_06(
        test_symbols,
        test_numbers,
        test_lowers,
        test_uppers
):
    """
    no upper case
    """
    pwd = create_password(
        16, test_symbols, test_numbers, test_lowers, test_uppers,
        1, 3, 12, 0
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
