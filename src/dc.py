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
import os
from config import config, Conf
from pathlib import Path
from nnunet.utilities.file_conversions import convert_3d_tiff_to_nifti
from nnunet.dataset_conversion.utils import generate_dataset_json
from tqdm import tqdm
from rich import print


def main(conf: Conf) -> None:
    """Main function."""
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

    # Train
    print("Converting training data...")
    for tr, ts in zip(tqdm(ims[:-5]), lbs[:-5]):
        if tr.stem != ts.stem:
            raise ValueError(f"Image {tr.stem} label {ts.stem} not match.")
        uni_name = tr.stem

        convert_3d_tiff_to_nifti(
            [tr.as_posix()],
            f"{target_imtr}/{uni_name}",
            (999, 1, 1),
            transform=lambda x: x[1:],
            is_seg=False,
        )
        convert_3d_tiff_to_nifti(
            [ts.as_posix()],
            f"{target_lbtr}/{uni_name}",
            (999, 1, 1),
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
            (999, 1, 1),
            transform=lambda x: x[1:],
            is_seg=False,
        )
        convert_3d_tiff_to_nifti(
            [ts.as_posix()],
            f"{target_lbts}/{uni_name}",
            (999, 1, 1),
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


if __name__ == "__main__":
    main(config)
