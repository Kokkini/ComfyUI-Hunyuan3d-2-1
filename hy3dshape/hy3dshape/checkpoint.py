"""Checkpoint loading compatibility for the Hunyuan 3D model files."""

from pathlib import Path

import torch

from comfy.utils import load_torch_file


# These are the legacy checkpoints published for Hunyuan 3D 2.1. They are
# trusted only because they are downloaded from the official Tencent model
# repository by this node. Keep ComfyUI's safe loader for every other file.
_TRUSTED_LEGACY_NAMES = {
    "hunyuan3d-dit-v2-1-fp16.ckpt",
    "hunyuan3d-dit-v2-1.ckpt",
    "hunyuan3d-vae-v2-1-fp16.ckpt",
    "hunyuan3d-vae-v2-1.ckpt",
}


def load_hunyuan_checkpoint(path):
    """Load a Hunyuan checkpoint without changing ComfyUI globally.

    The official Hunyuan 3D 2.1 .ckpt files use PyTorch's legacy tar
    serialization. ComfyUI's ``load_torch_file`` intentionally uses
    ``weights_only=True``, which cannot read that format. Fall back to the
    unrestricted loader only for the known official Hunyuan filenames.
    """
    checkpoint_path = Path(path)

    if checkpoint_path.name.lower() not in _TRUSTED_LEGACY_NAMES:
        return load_torch_file(str(checkpoint_path))

    return torch.load(
        str(checkpoint_path),
        map_location="cpu",
        weights_only=False,
    )
