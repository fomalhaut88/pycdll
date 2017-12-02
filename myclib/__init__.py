import os
import ctypes

from pycdll.compiler import Compiler


dll_dir = os.path.join(os.path.dirname(__file__), 'dll')
dll_path = Compiler.get_dllpath(dll_dir, 'myclib')

_dll = ctypes.CDLL(dll_path)


def sqr(n):
    c_n = ctypes.c_int(n)
    result = _dll.sqr(c_n)
    return result
