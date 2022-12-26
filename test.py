import base64

test: bytes = b'Basic YWRtaW46MTIzNA=='


def read_authentication(header_auth: bytes) -> list[str]:
    try:
        try:
            auth: str = header_auth.split()[1]
            login_data: list[str] = base64.b64decode(auth).decode().split(":")
            
            if login_data[1]:
                return login_data
        
        except AttributeError:
            return "BAD REQUEST", 400
    except IndexError:
        return "BAD REQUEST", 400


print(read_authentication(test))