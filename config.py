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
from dataclasses import dataclass, asdict, field
import os
from typing import cast
from rich import print
from smile_config import from_dataclass

@dataclass
class Conf:
    """Configuration for zebrafish."""

    name: str = "Task777_Zebrafish"

    database: str = "data/"

    raw: str = "raw/"
    raw_: str = ""
    preprocessed: str = "preprocessed/"
    preprocessed_: str = ""
    results: str = "results/"
    results_: str = ""

    cropped: str = "cropped/"

    ori: str = "data/3dpf raw/"
    seg: str = "data/3dpf segmented/"


    def __post_init__(self) -> None:
        """Post init."""
        set_env(self)

        self.raw_ = self.database + self.raw
        self.preprocessed_ = self.database + self.preprocessed
        self.results_ = self.database + self.results
        self.cropped_ = self.database + self.cropped

        os.makedirs(self.database, exist_ok=True)
        os.makedirs(self.raw_, exist_ok=True)
        os.makedirs(self.preprocessed_, exist_ok=True)
        os.makedirs(self.results_, exist_ok=True)
        os.makedirs(self.cropped_, exist_ok=True)


def set_env(conf: Conf) -> None:
    """Set environment."""
    os.environ["nnUNet_raw_data_base"] = conf.raw_
    os.environ["nnUNet_preprocessed"] = conf.preprocessed_
    os.environ["RESULTS_FOLDER"] = conf.results_


config = cast(Conf, from_dataclass(Conf()).config)


if __name__ == "__main__":
    print(asdict(config))
