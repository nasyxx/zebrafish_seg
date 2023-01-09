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
date     : Dec  22, 2022
email    : Nasy <nasyxx+python@gmail.com>
filename : config.py
project  : zebrafish
license  : GPL-3.0+

Configuration for zebrafish.
"""
# Standard Library
import os
from dataclasses import asdict, dataclass

# Types
from typing import Annotated, cast

# Utils
from rich import print

# Config
from smile_config import from_dataclass


@dataclass
class Conf:
    """Configuration for zebrafish."""

    task: Annotated[int, "nnUNet task ID."] = 777
    name: Annotated[str, "nnUNet task name"] = "Zebrafish"
    postfix: str = ""

    database: Annotated[str, "Dataset base path"] = "data/"

    raw: Annotated[str, "nnUNet raw data path"] = "raw/"
    preprocessed: Annotated[str, "nnUNet preprocessed data path"] = "preprocessed/"
    results: Annotated[str, "nnUNet results path"] = "results/"

    cropped: Annotated[str, "nnUNet cropped path"] = "cropped/"

    ori: Annotated[str, "Original photo dir."] = "data/ori/"
    seg: Annotated[str, "Segmented dir."] = "data/segmented/"

    space: Annotated[str, "Distance of each dim of the one pixel (T, H, W)"] = "1,1,1"

    tod: Annotated[bool, "Convert tif to dataset?"] = True
    tot: Annotated[bool, "Convert nii back to tif?"] = True

    in_: Annotated[str, "Dir of result of nii.gz "] = ""
    out_: Annotated[str, "Dir of results of tif dir"] = ""

    raw_: Annotated[str, "Alias, left empty"] = ""
    preprocessed_: Annotated[str, "Alias, left empty"] = ""
    results_: Annotated[str, "Alias, left empty"] = ""

    def __post_init__(self) -> None:
        """Post init."""
        set_env(self)

        self.raw_ = self.database + self.raw
        self.preprocessed_ = self.database + self.preprocessed
        self.results_ = self.database + self.results
        self.cropped_ = self.database + self.cropped

        self.name = f"Task{self.task}_{self.name}"

        if self.postfix:
            self.name += f"_{self.postfix}"

        os.makedirs(self.database, exist_ok=True)
        os.makedirs(self.raw_, exist_ok=True)
        os.makedirs(self.preprocessed_, exist_ok=True)
        os.makedirs(self.results_, exist_ok=True)
        os.makedirs(self.cropped_, exist_ok=True)

        with open("env.sh", "w") as f:
            f.write(
                f"export nnUNet_raw_data_base='{self.raw_}'\n"
                f"export nnUNet_preprocessed='{self.preprocessed_}'\n"
                f"export RESULTS_FOLDER='{self.results_}'\n"
            )


def set_env(conf: Conf) -> None:
    """Set environment."""
    os.environ["nnUNet_raw_data_base"] = conf.raw_
    os.environ["nnUNet_preprocessed"] = conf.preprocessed_
    os.environ["RESULTS_FOLDER"] = conf.results_


config = cast(Conf, from_dataclass(Conf()).config)


if __name__ == "__main__":
    print(asdict(config))
