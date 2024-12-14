"""
Integration tests for HTS launcher
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,invalid-name

import unittest
import pytest

from launcher.config import parse_config
from launcher.dispatch import Dispatcher


class TestStorageInterface(unittest.TestCase):
    @pytest.mark.only_run_with_direct_target
    def test_dev(self):
        config = parse_config("./tests/data/test_config.ini")
        dispatcher = Dispatcher(config, dryrun=True, disable_snapshot=True)
        new_dirs = dispatcher.get_new_directories()

        raise NotImplementedError()
