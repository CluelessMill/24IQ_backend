from icecream import ic
from cProfile import Profile
from pstats import Stats, SortKey


def test_function(function):
    def wrapper(*args, **kwargs):
        pr = Profile()
        pr.enable()
        res = function(*args, **kwargs)

        pr.disable()
        stats = Stats(pr)
        stats.sort_stats(SortKey.TIME)
        stats.dump_stats(filename=f"./api/tests_statistic/{function.__name__}.prof")
        return res

    return wrapper
