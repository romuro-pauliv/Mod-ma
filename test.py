token: str = None

try:
    try:
        real_token: list[str] = token.split()[1]
    except IndexError:
        print("INDEX ERROR")
except AttributeError:
    print("ATTRIBUTE ERROR")