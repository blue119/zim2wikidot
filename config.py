#!/usr/bin/env python
# coding=utf-8

import os
import re

CONFIG_DIRECTORY = 'zim2wikidot'
CONFIG_FORMAT = r'^.*\.txt$'

def read_config(config_file):
    config = {}

    # FIXME: handle open error
    with open(config_file, mode='rt') as f:
        for l in f:
            l = re.match(r'^([^#]*)#?.*$', l).group(1)

            if (re.match(r'^\s*$', l)):
                continue

            m = re.match(r'\s*([A-Za-z_-]+)\s*[:=](.*)$', l)

            assert m, 'config file error'

            config[m.group(1)] = m.group(2).strip()

    return config

def get_all_config(zim_root):
    directory = os.path.join(zim_root, CONFIG_DIRECTORY)

    assert os.path.exists(directory), 'no config directory'
    assert os.path.isdir(directory), 'no config directory'

    all_config = []

    for config_file in os.listdir(directory):
        if not re.match(CONFIG_FORMAT, config_file):
            continue

        config_file = os.path.join(directory, config_file)

        if not os.path.isfile(config_file):
            continue

        config = read_config(config_file)

        if config:
            all_config.append(config)

    return all_config
