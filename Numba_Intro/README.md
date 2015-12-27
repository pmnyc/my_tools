# Overview

Numba gives you the power to speed up your applications with high performance functions written directly in Python.

Numba is especially powerful when dealing with Numpy like scalar, vector and matrix calculations

Numba generates optimized machine code from pure Python code using the LLVM compiler infrastructure. With a few simple annotations, array-oriented and math-heavy Python code can be just-in-time optimized to performance similar as C, C++ and Fortran, without having to switch languages or Python interpreters.

Numba’s main features are:
* on-the-fly code generation (at import time or runtime, at the user’s preference)
* native code generation for the CPU (default) and GPU hardware
* integration with the Python scientific software stack (thanks to Numpy)

## Numba Installation on OS X
```shell
brew install llvm33 --rtti   #or install homebrew/versions/llvm33 if it did not work
git clone https://github.com/llvmpy/llvmpy.git
cd llvmpy
LLVM_CONFIG_PATH=/usr/local/lib/llvm-3.3/bin/llvm-config python setup.py install
python -c "import llvm; llvm.test()"
pip install numba
```