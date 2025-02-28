import secrets
import string


def generate_random_password(length: int = 32) -> str:
    """
    Generates a random password and returns it.

    Password requirements:

        - One lowercase letter
        - One uppercase letter
        - >= 3 digits
        - One special symbol

    :param length: Length for the randomly generated password.
    :type length: :py:obj:`int`
    :raises ValueError: If the provided length was less than 8.
    :raises ValueError: If the provided length was greater than 64.
    :returns: A randomly generated password.
    :rtype: :py:obj:`str`

    """
    min_length, max_length = 8, 64
    if length > max_length:
        raise ValueError(
            f"Password cannot be greater than {max_length} characters in length. Got {length} characters."
        )
    elif length < min_length:
        raise ValueError(
            f"Password cannot be less than {min_length} characters in length. Got {length} characters."
        )

    s0 = list(string.ascii_lowercase)
    s1 = list(string.ascii_uppercase)
    s2 = list(string.digits)
    s3 = list(string.punctuation)
    choices: list[str] = s0 + s1 + s2 + s3

    while True:
        password = "".join([secrets.choice(choices) for _ in range(length)])
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
            and any(c in s3 for c in password)
        ):
            break
    return password
