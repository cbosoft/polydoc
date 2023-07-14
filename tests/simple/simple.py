import math


def f(x):
    """
    params:
        - x :: numerical input to the fucntion
    returns:
        - sin(x)
    """
    return math.sin(x)


def g(x):
    """
    params:
        - x :: numerical input to the fucntion
    returns:
        - sin(x)
    """
    return math.sqrt(x)


# compare - runs a set of functions on a test input
# takes one or more functions as input
# returns x and the result of each function applied to x
def compare(*f):
    '''
    runs a set of functions on a test input
    takes one or more functions as input
    returns:
        - x and the result of each function applied to x
    '''
    x = [i*0.1 for i in range(11)]
    fs = [
        [f(xi) for xi in x]
    ]
    return x, fs


class Foo:
    """a class called foo, not to be confused with a thing called class. see [f](f), [g], [h]"""

    def __init__(self, bar):
        """init of Foo"""
        self.bar = bar

        self.baz = bar + 'BAZ'
