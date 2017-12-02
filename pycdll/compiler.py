import os
import sys
import shutil
import subprocess as sp
from contextlib import contextmanager


cwd = os.getcwd()


class CompilationError(Exception):
    pass


class Compiler:
    compiler = 'gcc'
    debug_name = 'debug'

    def __init__(self, c_dir, dll_dir, verbose=True):
        self.c_dir = os.path.join(cwd, c_dir)
        self.dll_dir = os.path.join(cwd, dll_dir)
        self.debug = os.path.join(cwd, self.debug_name)
        self.verbose = verbose

    def get_clibs(self):
        return os.listdir(self.c_dir)

    def compile(self, clib):
        clib_path = os.path.join(self.c_dir, clib)
        cpaths = self._get_cpaths(clib_path)

        with self._within_debug() as debug:
            # Compiling
            opaths = []
            for cpath in cpaths:
                cname = os.path.basename(cpath)
                oname = cname[:-2] + '.o'
                opath = os.path.join(debug, oname)
                self._compile(cpath, opath)
                opaths.append(opath)

            # Linking
            dllname = self._get_dllname(clib)
            dllpath = os.path.join(self.dll_dir, dllname)
            self._link(opaths, dllpath)

    def get_dlls(self):
        names = os.listdir(self.dll_dir)
        paths = list(map(
            lambda name: os.path.join(self.dll_dir, name),
            names
        ))
        return paths

    def collect_local_dlls(self):
        paths = self.get_dlls()
        local_paths = list(map(
            lambda path: os.path.relpath(path, cwd),
            paths
        ))
        return local_paths

    @classmethod
    def get_dllpath(cls, dll_dir, clib):
        dllname = cls._get_dllname(clib)
        return os.path.join(dll_dir, dllname)

    def _get_cpaths(self, path):
        cpaths = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.c'):
                    cpath = os.path.join(root, name)
                    cpaths.append(cpath)
        return cpaths

    @classmethod
    def _get_dllname(cls, clib):
        dll_ext = 'dll' if sys.platform == 'win32' else 'so'
        return clib + '.' + dll_ext

    def _compile(self, cpath, opath):
        command = "{compiler} -c -Wall -fPIC {cpath} -o {opath}".format(
            compiler=self.compiler, cpath=cpath, opath=opath
        )
        self._exec_bash(command)

    def _link(self, opaths, dllpath):
        command = "{compiler} -shared {opaths_str} -o {dllpath}".format(
            compiler=self.compiler, opaths_str=' '.join(opaths), dllpath=dllpath
        )
        self._exec_bash(command)

    def _exec_bash(self, command):
        if self.verbose:
            print(command)
        out, err = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
        if err:
            raise CompilationError(err.decode('utf-8'))

    @contextmanager
    def _within_debug(self):
        if os.path.exists(self.debug):
            shutil.rmtree(self.debug)
        os.mkdir(self.debug)
        yield self.debug
        shutil.rmtree(self.debug)
