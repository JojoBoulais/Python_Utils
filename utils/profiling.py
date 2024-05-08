import sys
import os
import functools
import time
from locations import AUTO_DELETED_DAILY
import uuid
from pstats import SortKey
import matplotlib
import matplotlib.pyplot as plt
import time
from collections.abc import Iterable


class profile(object):
    """
    Decorator for profiling a function that uses cprofile and pstats.

    ******************
    Usage:

    @profile("function name")
    def do_something():
        ...
    ******************
    ORDERING TYPES:

    calls, ncalls, cumtime, cumulative, filename, line, module, name, nfl, pcalls, stdname, time, tottime
    ******************
    RESULTS:

    ---------------------------------------------------
    ------------------ function name ------------------

    12248 function calls (118408 primitive calls) in 0.546 seconds
    ...
    ---------------------------------------------------

    """

    def __init__(self, print_stats=(55,),
                 sort_status=SortKey.TIME,
                 whrf=False,
                 stats_file=False):
        """
        :param tuple print_stats:
        :param SortKey strsort_status:
        :param bool whrf: write human readable file or not.
        :param bool stats_file: write stats file or not.
        """

        self.print_stats = print_stats
        self.sort_status = sort_status
        self.whrf = whrf #

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            import cProfile

            # profile here
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            import pstats

            # Print here
            title = f"\t{'-' * (62 + len(func.__name__))}\n\t{'-' * 30} {func.__name__} {'-' * 30}\n\n"
            bottom = f"\t{'-' * (62 + len(func.__name__))}\n"
            sys.stdout.write(title)
            stats = pstats.Stats(pr, stream=sys.stdout)
            stats.sort_stats(self.sort_status)
            stats.print_stats(*self.print_stats)
            sys.stdout.write(bottom)

            # write to files here
            _uuid = uuid.uuid4().hex
            stats_file = os.path.join(AUTO_DELETED_DAILY, func.__name__ + "_" + _uuid + ".stats")
            stats.dump_stats(stats_file)
            print(f"Stats file: '{stats_file}'\n")
            if self.whrf:
                hrf = os.path.join(AUTO_DELETED_DAILY, func.__name__ + "_" + _uuid + ".txt")
                with open(hrf, "a") as f:
                    f.write(title)
                    stats.stream = f
                    stats.print_stats(*self.print_stats)
                    f.write(bottom)
                    print(f"Human readable file: '{hrf}'")
            return result

        return wrapped_func


class avrg_time(object):
    def __init__(self, iters):
        """

        :param int iters: number of time to run the function.
        """
        self.iters = iters

    def __call__(self, func):

        def wrapped_func(*args, **kwargs):
            s_time = time.time()
            for i in range(0, self.iters):
                func(*args, **kwargs)
            e_time = time.time()
            print(f"\t{'-' * (62 + len(func.__name__))}\n\t{'-' * 30} {func.__name__} {'-' * 30}\n")
            print(f"\tCalled: {self.iters} times.\n")
            print(f"\tTotal time: {e_time-s_time}\n")
            print(f"\tAverage Time: {(e_time-s_time)/float(self.iters)}")
            print(f"\t{'-' * (62 + len(func.__name__))}\n")
        return wrapped_func

class matplotthis(object):
    """Requires iterable arguments to amplify there content."""

    def __init__(self, iterations, amp_factor=10):
        self.iterations = iterations
        self.amp_factor = amp_factor

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):

            for i in range(1, self.iterations):

                new_args = []
                taille_problem = 0
                # Amplifying any Iterable argument
                for arg in args:
                    if isinstance(arg, Iterable):
                        amplified_arg = arg * self.amp_factor * i
                        new_args.append(amplified_arg)
                        taille_problem += len(amplified_arg)
                    else:
                        new_args.append(arg)
                start_time = time.time()
                func(*new_args, **kwargs)
                end_time = time.time() - start_time
                plt.scatter(taille_problem, end_time, alpha=0.3, edgecolors='none')

            plt.title(f"Calling '{func.__name__}' x{self.iterations} times.")
            plt.xlabel("Taille du probleme")
            plt.ylabel("Time (sec)")

            plt.show()
        return wrapped_func
