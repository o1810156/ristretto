# Randomized Dimension Reduction Library


NAME ='DimLy'
VERSION ='0.0.1'
DESCRIPTION ='Randomized Dimension Reduction Library'
URL ='https://github.com/Benli11/DimLy'
AUTHER ='N. Benjamin Erichson'
EMAIL ='erichson at uw dot edu'
LICENSE ='GNU'


      
# Install setuptools if it isn't available:     
try:
    from setuptools import setup, find_packages
except ImportError:
    print "The package 'setuptools' is required!"

from distutils.command.clean import clean as Clean
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True


# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Custom clean command to remove build artifacts
# as used by scikit-learn
# https://github.com/scikit-learn/scikit-learn/blob/master/setup.py
class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, 'PKG-INFO'))
        if remove_c_files:
            print('Will remove generated .c files')
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('sklearn'):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if remove_c_files and extension in ['.c', '.cpp']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


cmdclass = {'clean': CleanCommand}


cmdclass = { }
ext_modules = [ ]

if use_cython:
    ext_modules += [
        Extension("dimly._fhals_update", [ "dimly/nmf/_fhals_update.pyx" ]),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("dimly._fhals_update", [ "dimly/nmf/_fhals_update.c" ]),
    ]



setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    url = URL,
    author = AUTHER,
    author_email = EMAIL,
    license = LICENSE,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Researchers',
        'Topic :: Randomized Linear Algebra :: Tensor Decompositions',

        # Pick your license as you wish (should match "license" above)
        'License :: GNU',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='randomized algorithms, dimension reduction, tensor decomposition',

    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=find_packages(exclude=['tests*']),
    test_suite='nose.collector',	

	# cythonize
    cmdclass = cmdclass,
    ext_modules = ext_modules
)



