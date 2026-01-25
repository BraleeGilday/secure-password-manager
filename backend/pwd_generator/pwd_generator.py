import random


def generate_password(
        length: int = 16,
        has_symbols: bool = True,
        has_numbers: bool = True,
        mixed_case: bool = True
) -> str:
    """
    Generates a randomized string based on flags passed by user
    length = 16 (default)
    has_symbols = include symbols (default)
    has_numbers = include digits (default)
    mixed_case = include upper and lower roman english letters (default)
    """
    (alphabet, symbols, numbers,
     total_symbols, total_numbers, total_letters
     ) = create_alphabet(
         length,
         has_symbols,
         has_numbers,
         mixed_case
        )

    return create_password(
        length, symbols, numbers,
        alphabet, total_symbols, total_numbers,
        total_letters,
    )


def create_alphabet(
        length: int,
        has_symbols: bool,
        has_numbers: bool,
        mixed_case: bool
        ) -> tuple[str, str, str, int, int, int]:
    """
    Create the alphabet for the password generator
    """
    # should split into upper and lower and require at least 1 char each?
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    symbols = ""
    numbers = ""

    total_symbols, total_numbers = 0, 0
    # at least 1, at most (length of pwd / 4) digits or symbols
    max_special_chars = length // 4

    if has_symbols:
        total_symbols = random.randint(1, max_special_chars)
        symbols = "~!@#$%^&*()-_+=,.?:;"

    if has_numbers:
        total_numbers = random.randint(1, max_special_chars)
        numbers = "1234567890"

    if not mixed_case:
        alphabet = "abcdefghijklmnopqrstuvwxyz"

    total_letters = length - total_symbols - total_numbers

    return (alphabet, symbols, numbers,
            total_symbols, total_numbers, total_letters)


def create_password(
        length: int,
        symbols: str,
        numbers: str,
        alphabet: str,
        total_symbols: int,
        total_numbers: int,
        total_letters: int,
) -> str:
    """
    Creates the final password string
    """

    password = []

    while len(password) != length:
        if total_symbols > 0:
            password.append(random.choice(symbols))
            total_symbols -= 1
        if total_numbers > 0:
            password.append(random.choice(numbers))
            total_numbers -= 1
        if total_letters > 0:
            password.append(random.choice(alphabet))
            total_letters -= 1

    random.shuffle(password)
    return "".join(password)
