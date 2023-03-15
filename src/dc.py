#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Dec  22, 2023
email    : Nasy <nasyxx+python@gmail.com>
filename : dc.py
project  : zebrafish
license  : GPL-3.0+

Data converter.
"""
# Standard Library
import os
from pathlib import Path

# Utils
from rich import print
from rich.prompt import Confirm
from tqdm import tqdm

# Config
from config import Conf, config

# Others
import tifffile
from nnunet.dataset_conversion.utils import generate_dataset_json
from nnunet.utilities.file_conversions import (
    convert_3d_segmentation_nifti_to_tiff,
    convert_3d_tiff_to_nifti,
)


def to_dataset(conf: Conf) -> None:
    """Convert to dataseit."""
    dbase = f"{conf.raw_}nnUNet_raw_data/{conf.name}"
    target_imtr = f"{dbase}/imagesTr"
    target_imts = f"{dbase}/imagesTs"
    target_lbtr = f"{dbase}/labelsTr"
    target_lbts = f"{dbase}/labelsTs"

    os.makedirs(target_imtr, exist_ok=True)
    os.makedirs(target_imts, exist_ok=True)
    os.makedirs(target_lbtr, exist_ok=True)
    os.makedirs(target_lbts, exist_ok=True)

    ims = sorted(Path(conf.ori).glob("*.tif"))
    lbs = sorted(Path(conf.seg).glob("*.tif"))

    space = tuple(conf.space.split(","))

    # Train
    print("Converting training data...")
    for tr, ts in zip(tqdm(ims[:-5]), lbs[:-5]):
        if tr.stem != ts.stem:
            raise ValueError(f"Image {tr.stem} label {ts.stem} not match.")
        uni_name = tr.stem

        convert_3d_tiff_to_nifti(
            [tr.as_posix()],
            f"{target_imtr}/{uni_name}",
            space,
            transform=lambda x: x[1:],  # NOTE: We igoore the first slice in image, since it has 184 slice vs label has 183.
            is_seg=False,
        )
        convert_3d_tiff_to_nifti(
            [ts.as_posix()],
            f"{target_lbtr}/{uni_name}",
            space,
            transform=lambda x: (x == 255).astype(int),
            is_seg=True,
        )

    # Test
    print("Converting testing data...")
    for tr, ts in zip(tqdm(ims[-5:]), lbs[-5:]):
        if tr.stem != ts.stem:
            raise ValueError(f"Image {tr.stem} label {ts.stem} not match.")
        uni_name = tr.stem

        convert_3d_tiff_to_nifti(
            [tr.as_posix()],
            f"{target_imts}/{uni_name}",
            space,
            transform=lambda x: x[1:],  # NOTE: We igoore the first slice in image, since it has 184 slice vs label has 183.
            is_seg=False,
        )
        convert_3d_tiff_to_nifti(
            [ts.as_posix()],
            f"{target_lbts}/{uni_name}",
            space,
            transform=lambda x: (x == 255).astype(int),
            is_seg=True,
        )

    generate_dataset_json(
        f"{dbase}/dataset.json",
        target_imtr,
        target_imts,
        ("x",),
        labels={0: "background", 1: "cell"},
        dataset_name=conf.name,
    )


def to_tiff(in_: str, out_: str) -> None:
    """From nii To tiff."""
    for nii in tqdm(tuple(Path(in_).glob("*.nii.gz"))):
        base = Path(nii.stem).stem
        convert_3d_segmentation_nifti_to_tiff(nii.as_posix(), f"{out_}/{base}.tif")

        tifffile.imwrite(f"{out_}/{base}.tif", tifffile.imread(f"{out_}/{base}.tif") * 255)


if __name__ == "__main__":
    print(config)

    if config.tod:
        if Confirm.ask("Convert to dataset?"):
            to_dataset(config)

    if config.tot and config.in_ and config.out_:
        if Confirm.ask("Convert to tiff?"):
            to_tiff(config.in_, config.out_)
