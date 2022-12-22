import re

email_input: str = input("EMAIL ADDRESS: ")

def email_validation(email: str) -> tuple[str, int]:
    regex: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return ("VALID EMAIL", 202) if re.fullmatch(regex, email) else ("INVALID EMAIL", 400)


print(email_validation(email_input))
