import ctypes
from pycdll.compiler import Compiler

cpl = Compiler(dll_dir='dll')
dllpath = cpl.get_dll('myclib')

dll = ctypes.CDLL(dllpath)

n = ctypes.c_int(5)
result = dll.sqr(n)
print(result)
