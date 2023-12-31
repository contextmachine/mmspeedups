# setup.py
import os
import sys
import shutil
from pathlib import Path


from setuptools import setup, Extension


from setuptools.command.build_ext import build_ext
os.environ["CODON_PYTHON"] = os.environ["CODON_CPYTHON"] = \
    "/opt/homebrew/Frameworks/Python.framework/Versions/3.11/lib/libpython3.11.dylib"
HOME=os.getenv('HOME')
os.environ["CODON_DIR"]=f"{HOME}/.codon"
sys.path.extend([f"{HOME}/.codon/bin",
                 f"{HOME}/.codon",
                 '/opt/homebrew/Frameworks/Python.framework/Versions/3.11',
                 '/opt/homebrew/Frameworks/Python.framework/Versions/3.11/bin',
'/usr/local/lib/'


                 ])
# Find Codon
print(HOME)
codon_path = f"{HOME}/.codon"
if not codon_path:
    c = shutil.which('codon')
    if c:
        codon_path = Path(c).parent / '..'
else:
    codon_path = Path(codon_path)
for path in [
    os.path.expanduser('~') + '/.codon',
    os.getcwd() + '/..',
]:
    path = Path(path)
    if not codon_path and path.exists():
        codon_path = path
        break

if (
    not codon_path
    or not (codon_path / 'include' / 'codon').exists()
    or not (codon_path / 'lib' / 'codon').exists()
):
    print(
        f'{codon_path}'
        'Cannot find Codon.',
        'Please either install Codon (https://github.com/exaloop/codon),',
        'or set CODON_DIR if Codon is not in PATH.',
        file=sys.stderr,
    )
    sys.exit(1)
codon_path = codon_path.resolve()
print('Found Codon:', str(codon_path))

# Build with Codon
class CodonExtension(Extension):
    def __init__(self, name, source):
        self.source = source
        super().__init__(name, sources=[], language='c')

class BuildCodonExt(build_ext):
    def build_extensions(self):
        pass

    def run(self):
        inplace, self.inplace = self.inplace, False
        super().run()
        for ext in self.extensions:
            self.build_codon(ext)
        if inplace:
            self.copy_extensions_to_source()

    def build_codon(self, ext):
        extension_path = Path(self.get_ext_fullpath(ext.name))
        build_dir = Path(self.build_temp)
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        codon_cmd = str(codon_path / 'bin' / 'codon')
        optimization = '-release'
        self.spawn([codon_cmd, 'build', optimization, '--relocation-model=pic', '-pyext',
                    '-o', str(extension_path) + ".o", '-module', ext.name, ext.source])

        ext.runtime_library_dirs = [str(codon_path / 'lib' / 'codon')]
        self.compiler.link_shared_object(
            [str(extension_path) + '.o'],
            str(extension_path),
            libraries=['codonrt'],
            library_dirs=ext.runtime_library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_preargs=['-Wl,-rpath,@loader_path'],
            debug=False,
            build_temp=self.build_temp,
        )
        self.distribution.codon_lib = extension_path

setup(
    name='mmvec',
    version='0.1.10',
    packages=['mmvec'],
    ext_modules=[

        CodonExtension('mmvec', 'mmvec/__init__.codon'),


    ],
    platforms=["macos/universal","macos/x64","macos/arm64","linux/x64", "manylinux/x64"],
    cmdclass={'build_ext': BuildCodonExt}
)

setup(
    name='mmtests',
    version='0.1.5',
    packages=['mmtests'],
    ext_modules=[

        CodonExtension('mmtests', 'mmtests/__init__.codon'),


    ],
    platforms=["macos/universal","macos/x64","macos/arm64","linux/x64", "manylinux/x64"],

    cmdclass={'build_ext': BuildCodonExt}
)