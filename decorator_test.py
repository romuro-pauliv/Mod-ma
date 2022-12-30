from typing import Callable, Any


class IAM(object):
    @staticmethod
    def check_permission(method: str, structure: str) -> None:
        
        def Inner(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args, **kwargs) -> Callable[..., Any]:
                print(method, structure)
                return func(*args, **kwargs)
            
            return wrapper
        return Inner

@IAM.check_permission("testing", "helloe")
def som(x, y) -> None:
    print(x + y)


som(123, 321)