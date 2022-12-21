import string

input_password: str = input("INPUT THE PASSWORD: ")

def password_validation(passwd: str) -> tuple[str, bool]:
    type_char: list[str] = ['lowercase', 'uppercase', 'digits', 'punctuation']

    count: dict[str, int] = {
        "lowercase": 0,
        "uppercase": 0,
        "digits": 0,
        "punctuation": 0
    }
    
    ascii_base: dict[str] = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "punctuation": string.punctuation
    }

    if len(passwd) >= 8:
        for _char in passwd:
            for tc in type_char:
                if _char in ascii_base[tc]:
                    count[tc] += 1
    else:
        return "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS", False

    for tc in type_char:
        if count[tc] < 1:
            return str("MISSING 1 " + tc.upper() + " CHARACTER"), False
    
    return "PASSWORD VALID", True, passwd

input_pass = password_validation(input_password)
confirm_pass = input("CONFIRM PASS: ")

if confirm_pass == input_pass[2]:
    print(True)