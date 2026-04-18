SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")


def validate_password(password):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if sum(character.isdigit() for character in password) < 2:
        errors.append("The password must contain at least 2 numbers")

    if not any(character.isupper() for character in password):
        errors.append("password must contain at least one capital letter")

    if not any(character in SPECIAL_CHARACTERS for character in password):
        errors.append("password must contain at least one special character")

    return {"is_valid": not errors, "errors": errors}
