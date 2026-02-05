import re


def validar_contrasena(contra: str) -> bool:
    return (
        len(contra) >= 8
        and re.search(r"[A-Z]", contra)
        and re.search(r"[a-z]", contra)
        and re.search(r"\d", contra)
        and re.search(r"[!@#$%^&*()\-_=+{}\[\]|\\;:'\",.<>/?]", contra)
    )


def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
