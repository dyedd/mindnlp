# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
AG_NEWS load function
"""
# pylint: disable=C0103

import os
import csv
from typing import Union, Tuple
from mindspore.dataset import GeneratorDataset
from mindnlp.utils.download import cache_file
from mindnlp.dataset.register import load
from mindnlp.configs import DEFAULT_ROOT

URL = {
    "train": "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv",
    "test": "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/test.csv",
}

MD5 = {
    "train": "b1a00f826fdfbd249f79597b59e1dc12",
    "test": "d52ea96a97a2d943681189a97654912d",
}

class Agnews:
    """
    AG_NEWS dataset source
    """

    def __init__(self, path):
        self.path = path
        self._label, self._text = [], []
        self._load()

    def _load(self):
        csvfile = open(self.path, "r", encoding="utf-8")
        dict_reader = csv.reader(csvfile)
        for row in dict_reader:
            self._label.append(row[0])
            self._text.append(f"{row[1]} {row[2]}")

    def __getitem__(self, index):
        return self._label[index], self._text[index]

    def __len__(self):
        return len(self._text)

@load.register
def AG_NEWS(root: str = DEFAULT_ROOT, split: Union[Tuple[str], str] = ("train", "test")):
    r"""
    Load the AG_NEWS dataset
    Args:
        root (str): Directory where the datasets are saved.
            Default:~/.mindnlp
        split (str|Tuple[str]): Split or splits to be returned.
            Default:('train', 'test').

    Returns:
        - **datasets_list** (list) -A list of loaded datasets.
            If only one type of dataset is specified,such as 'trian',
            this dataset is returned instead of a list of datasets.

    Examples:
        >>> root = os.path.join(os.path.expanduser('~'), ".mindnlp")
        >>> dataset_train,dataset_test = agnews()
        >>> train_iter = dataset_train.create_tuple_iterator()
        >>> print(next(train_iter))
        [Tensor(shape=[], dtype=String, value= '3'), Tensor(shape=[], dtype=String,\
             value= "Wall St. Bears Claw Back Into the Black (Reuters) Reuters - \
            Short-sellers, Wall Street's dwindling\\band of ultra-cynics, are seeing green again.")]

    """

    cache_dir = os.path.join(root, "datasets", "AG_NEWS")
    column_names = ["label", "text"]
    datasets_list = []
    path_list = []
    if isinstance(split,str):
        path, _ = cache_file(None, url=URL[split], cache_dir=cache_dir, md5sum=MD5[split])
        path_list.append(path)
    else:
        for s in split:
            path, _ = cache_file(None, url=URL[s], cache_dir=cache_dir, md5sum=MD5[s])
            path_list.append(path)
    for path in path_list:
        datasets_list.append(GeneratorDataset(source=Agnews(path), column_names=column_names, shuffle=False))
    if len(path_list) == 1:
        return datasets_list[0]
    return datasets_list