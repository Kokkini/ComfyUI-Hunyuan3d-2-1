# Hunyuan 3D is licensed under the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT
# except for the third-party components listed below.
# Hunyuan 3D does not impose any additional limitations beyond what is outlined
# in the repsective licenses of these third-party components.
# Users must comply with all terms and conditions of original licenses of these third-party
# components and must ensure that the usage of the third party components adheres to
# all relevant laws and regulations.

# For avoidance of doubts, Hunyuan 3D means the large language models and
# their software and algorithms, including trained model weights, parameters (including
# optimizer states), machine-learning model code, inference-enabling code, training-enabling code,
# fine-tuning enabling code and other elements of the foregoing made publicly available
# by Tencent in accordance with TENCENT HUNYUAN COMMUNITY LICENSE AGREEMENT.

from setuptools import setup, find_packages
from pathlib import Path
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension

# build custom rasterizer

# The CUDA runtime wheels used by PyTorch provide the versioned library
# headers under site-packages/nvidia.  Include them when present so a local
# toolkit installation only needs to provide nvcc and the core CUDA headers.
site_packages = Path(torch.__file__).resolve().parent.parent
cuda_dependency_includes = [
    str(site_packages / "nvidia" / package / "include")
    for package in ("cublas", "cusolver", "cusparse")
    if (site_packages / "nvidia" / package / "include").is_dir()
]

custom_rasterizer_module = CUDAExtension(
    "custom_rasterizer_kernel",
    [
        "lib/custom_rasterizer_kernel/rasterizer.cpp",
        "lib/custom_rasterizer_kernel/grid_neighbor.cpp",
        "lib/custom_rasterizer_kernel/rasterizer_gpu.cu",
    ],
    extra_compile_args={
        # PyTorch's Windows extension builder supplies /std:c++17.  Keep the
        # host compiler flags in MSVC syntax so they are not silently ignored.
        "cxx": ["/O2"],
        "nvcc": ["-O3"],
    },
    include_dirs=cuda_dependency_includes,
)

setup(
    packages=find_packages(),
    version="0.1",
    name="custom_rasterizer",
    include_package_data=True,
    package_dir={"": "."},
    ext_modules=[
        custom_rasterizer_module,
    ],
    cmdclass={"build_ext": BuildExtension},
)
