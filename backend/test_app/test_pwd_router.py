from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_pwd_01(count_characters):
    """
    test default params
    """
    response = client.post("/spm/password/generate", json={})
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols > 0
    assert numbers > 0
    assert len(pwd) == 16
    assert (len(pwd) - symbols - numbers) == (lowers + uppers)


def test_generate_pwd_02(count_characters):
    """
    test passed length
    """
    response = client.post("/spm/password/generate", json={
        "length": 32,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols > 0
    assert numbers > 0
    assert len(pwd) == 32
    assert (len(pwd) - symbols - numbers) == (lowers + uppers)


def test_generate_pwd_03(count_characters):
    """
    no symbols
    """
    response = client.post("/spm/password/generate", json={
        "has_symbols": False,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols == 0
    assert numbers > 0
    assert len(pwd) == 16
    assert (len(pwd) - symbols - numbers) == (lowers + uppers)


def test_generate_pwd_04(count_characters):
    """
    no numbers
    """
    response = client.post("/spm/password/generate", json={
        "has_numbers": False,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols > 0
    assert numbers == 0
    assert len(pwd) == 16
    assert (len(pwd) - symbols - numbers) == (lowers + uppers)


def test_generate_pwd_05(count_characters):
    """
    length 24, no symbols, no numbers, no mixed case
    NB - Used co-pilot to generate test cases 5 - 10
    """
    response = client.post("/spm/password/generate", json={
        "length": 24,
        "has_symbols": False,
        "has_numbers": False,
        "mixed_case": False,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols == 0
    assert numbers == 0
    assert len(pwd) == 24
    assert uppers == 0
    assert lowers == 24


def test_generate_pwd_06(count_characters):
    """
    length 16, symbols, numbers, no mixed case
    """
    response = client.post("/spm/password/generate", json={
        "length": 16,
        "has_symbols": True,
        "has_numbers": True,
        "mixed_case": False,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert symbols > 0
    assert numbers > 0
    assert len(pwd) == 16
    assert uppers == 0
    assert lowers == (len(pwd) - symbols - numbers)


def test_generate_pwd_07(count_characters):
    """
    minimum length (8 characters)
    """
    response = client.post("/spm/password/generate", json={
        "length": 8,
    })
    pwd = response.json()["password"]
    symbols, numbers, lowers, uppers = count_characters(pwd)

    assert response.status_code == 200
    assert len(pwd) == 8
    assert symbols > 0
    assert numbers > 0


def test_generate_pwd_08():
    """
    maximum length (64 characters)
    """
    response = client.post("/spm/password/generate", json={
        "length": 64,
    })
    pwd = response.json()["password"]

    assert response.status_code == 200
    assert len(pwd) == 64


def test_generate_pwd_09():
    """
    length below minimum (should fail)
    """
    response = client.post("/spm/password/generate", json={
        "length": 7,
    })

    assert response.status_code == 422  # Validation error


def test_generate_pwd_10():
    """
    length above maximum (should fail)
    """
    response = client.post("/spm/password/generate", json={
        "length": 65,
    })

    assert response.status_code == 422  # Validation error
