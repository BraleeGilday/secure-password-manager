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
    (lowers, uppers, symbols, numbers,
     total_symbols, total_numbers, total_lowers, total_uppers
     ) = create_alphabet(
         length,
         has_symbols,
         has_numbers,
         mixed_case
        )

    return create_password(
        length,
        symbols,
        numbers,
        lowers,
        uppers,
        total_symbols,
        total_numbers,
        total_lowers,
        total_uppers
    )


def create_alphabet(
        length: int,
        has_symbols: bool,
        has_numbers: bool,
        mixed_case: bool
        ) -> tuple[str, str, str, str, int, int, int, int]:
    """
    Create the alphabet for the password generator
    """
    # should split into upper and lower and require at least 1 char each?
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowers = "abcdefghijklmnopqrstuvwxyz"
    symbols = ""
    numbers = ""
    max_uppers = random.randint(1, length // 2)
    total_uppers = max(1, max_uppers)
    total_lowers = 0
    total_symbols, total_numbers = 0, 0

    # at least 1, at most (length of pwd / 4) digits or symbols
    max_special_chars = max(1, length // 4)

    if has_symbols:
        total_symbols = random.randint(1, max_special_chars)
        symbols = "~!@#$%^&*()-_+=,.?:;"

    if has_numbers:
        total_numbers = random.randint(1, max_special_chars)
        numbers = "1234567890"

    total_lowers = length - total_symbols - total_numbers - total_uppers

    if not mixed_case:
        total_uppers = 0
        total_lowers = length - total_symbols - total_numbers
        uppers = ""

    return (lowers, uppers, symbols, numbers,
            total_symbols, total_numbers, total_lowers, total_uppers)


def create_password(
        length: int,
        symbols: str,
        numbers: str,
        lowers: str,
        uppers: str,
        total_symbols: int,
        total_numbers: int,
        total_lowers: int,
        total_uppers: int,
) -> str:
    """
    Creates the final password string
    """

    password = []
    
    for _ in range(length):
        if total_symbols > 0:
            password.append(random.choice(symbols))
            total_symbols -= 1
        if total_numbers > 0:
            password.append(random.choice(numbers))
            total_numbers -= 1
        if total_lowers > 0:
            password.append(random.choice(lowers))
            total_lowers -= 1
        if total_uppers > 0:
            password.append(random.choice(uppers))
            total_uppers -= 1

    random.shuffle(password)
    return "".join(password)


def evaluate_strength(
        length: int,
        symbols: int,
        numbers: int,
        uppers: int,
        lowers: int
        ) -> str:
    """
    Return strength rating of password (does not acct for common words)
    """
    guidelines = {0: "very weak", 1: "weak", 2: "medium-weak",
                  3: "medium", 4: "strong", 5: "very strong"}
    strength = 0
    if 7 < length < 17:
        strength += 1
    if symbols > 0:
        strength += 1
    if numbers > 0:
        strength += 1
    if uppers > 0:
        strength += 1
    if lowers > 0:
        strength += 1

    return guidelines[strength]
