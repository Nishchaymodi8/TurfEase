import re

class email_validator:
    def validate(email: str) -> bool:
        pattern = r"^([A-Za-z0-9]+[._+\-]?)+[A-Za-z0-9]+@([A-Za-z0-9]+[.\-]?)+[A-Za-z0-9]+\.[A-Za-z0-9]+$"
        return re.search(pattern, email) is not None


class password_validator:
    def validate(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"\W", password):
            return False
        return True
