from app.hello import greeting


def test_greeting():
    assert greeting("Python") == "Hola, Python!"
