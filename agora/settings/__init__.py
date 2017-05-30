import os


def _type():
    if "AGORAPROD" in os.environ is not None:
        return "production"

    return "testing"


exec("from .{} import *".format(_type()))
