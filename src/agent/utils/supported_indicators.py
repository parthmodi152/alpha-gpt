import sympy as sp


# Define placeholder functions for SymPy
def SMA(*args):
    return sp.Function("SMA")(*args)


def EMA(*args):
    return sp.Function("EMA")(*args)


def RSI(*args):
    return sp.Function("RSI")(*args)


def ATR(*args):
    return sp.Function("ATR")(*args)


def BollingerBandsWidth(*args):
    return sp.Function("BollingerBandsWidth")(*args)


def correlation(*args):
    return sp.Function("correlation")(*args)


def ln(*args):
    return sp.log(*args)


def sqrt(*args):
    return sp.sqrt(*args)


# Map supported indicators to callable functions
SUPPORTED_INDICATORS = {
    "SMA": SMA,
    "EMA": EMA,
    "RSI": RSI,
    "ATR": ATR,
    "BollingerBandsWidth": BollingerBandsWidth,
    "correlation": correlation,
    "ln": sp.log,
    "log": sp.log,
    "sqrt": sp.sqrt,
}
