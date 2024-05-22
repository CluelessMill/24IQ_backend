from icecream import ic
from cProfile import Profile
from pstats import Stats, SortKey


def test_function(function):
    """
    Decorator for profiling a function's execution time

    Parameters:
        function (callable): The function to be profiled

    Returns:
        callable: The wrapped function

    Raises:
        None
    """
    def wrapper(*args, **kwargs):
        pr = Profile()
        pr.enable()
        ic(function.__name__)
        res = function(*args, **kwargs)

        pr.disable()
        stats = Stats(pr)
        stats.sort_stats(SortKey.TIME)
        stats.dump_stats(filename=f"./src/api/tests_statistic/{function.__name__}.prof")
        return res

    return wrapper
