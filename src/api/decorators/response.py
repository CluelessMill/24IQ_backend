from icecream import ic
from rest_framework.response import Response


def response_handler(function):
    """
    Decorator for handling responses and exceptions gracefully

    Parameters:
        function (callable): The function to be wrapped

    Returns:
        callable: The wrapped function

    Raises:
        None
    """
    def wrapper(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
            return res
        except ValueError as e:
            return Response({"message": str(e)}, status=400)
        except Exception as e:
            return Response({"message": "An error occured"}, status=500)

    return wrapper
