from pycdll.compiler import Compiler

cpl = Compiler(
    c_dir='c',
    dll_dir='myclib/dll'
)
cpl.compile('myclib')
