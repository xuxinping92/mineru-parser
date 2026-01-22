# mineru_parser/auth.py

import os
from getpass import getpass


def ensure_env(var: str, prompt: str | None = None) -> str:
    """
    Ensure an environment variable exists.
    If not, prompt user to input it securely.

    Returns:
        str: the value of the environment variable
    """
    value = os.environ.get(var)

    if not value:
        prompt = prompt or f"Enter your {var}: "
        value = getpass(prompt)
        os.environ[var] = value

    return value
