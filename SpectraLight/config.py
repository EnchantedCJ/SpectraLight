# -*- coding: utf-8 -*-
import json


def read_config(configPath):
    with open(configPath, 'r', encoding='utf-8') as f:
        configText = f.read()
    config = json.loads(configText)
    return config
