"""
Simple set of functions for outputting JSON files.
"""

from __future__ import print_function
import json
import os

def merge(target, source):
    """Helper function: return the deep merge of `target` and `source`."""
    target = dict(target)
    for k in source:
        if isinstance(target.get(k), dict) and isinstance(source.get(k), dict):
            target[k] = merge(target[k], source[k])
        else:
            target[k] = source[k]
    return target

class RunInfo(object):
    def __init__(self, base_path):
        self.base_path = base_path
        self.stats = {}
        self.log = {}

    def write_args(self, args):
        """
        Save `args` (returned from `ArgumentParser.parse_args()`) to a file.
        """
        with open(os.path.join(self.base_path, 'args.json'), 'w') as f:
            print(json.dumps(vars(args), indent=2), file=f)

    def update_stats(self, new_stats):
        """
        Recursively merge `new_stats` and write it out to a file.
        """
        self.stats = merge(self.stats, new_stats)
        with open(os.path.join(self.base_path, 'stats.json'), 'w') as f:
            print(json.dumps(self.stats, indent=2), file=f)

    def update_log(self, new_log):
        """
        Recursively merge `new_log` and write it out to a file.
        """
        self.log = merge(self.log, new_log)
        with open(os.path.join(self.base_path, 'log.json'), 'w') as f:
            print(json.dumps(self.log, indent=2), file=f)
