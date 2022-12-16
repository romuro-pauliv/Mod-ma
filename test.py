from typing import Union, Callable, Any


def log_delete(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple[str, int]]]:
    def wrapper(*args, **kwargs) -> Callable[[str], tuple[str, int]]:
        val: Callable[[str], tuple[str, int]] = func(*args, **kwargs)
        print("args", args)
        print("kwargs", kwargs)

        return val
    return wrapper


@log_delete
def document(database: str, collection: str, _id: str) -> tuple[str, int]:
    arguments: list[str] = [database, collection, _id]
    for arg in arguments:
        print(">>> system: {}".format(arg))
    
    return "CREATED", 200


document("DATABASE", "COLLECTION", "123123123123")
