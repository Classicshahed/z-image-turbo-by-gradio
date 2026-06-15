@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
set "PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin"
set CMAKE_ARGS=-DSD_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DCMAKE_CUDA_FLAGS="-allow-unsupported-compiler -D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH" -DCMAKE_CXX_FLAGS="-D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH" -DCMAKE_C_FLAGS="-D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH"
set CMAKE_GENERATOR=Ninja
set CUDACXX=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin\nvcc.exe
venv\Scripts\python.exe -m pip install stable-diffusion-cpp-python --force-reinstall --no-cache-dir
