from functools import wraps
   

def good_decorator(function):
    @wraps(function)
    def inner(self):
        return function(self) + ' good'
    return inner





def require_validation():
    def decorator(function):
        def inner(t):
            glob = t
            if glob:
                return function(t)
            else:
                return False
        return inner
    return decorator

@require_validation()
def hello(t):
    return "Text"


if __name__ == '__main__':
    print(hello(False))