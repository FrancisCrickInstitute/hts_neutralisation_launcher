"""
Integration tests for HTS launcher
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,invalid-name

import os
import unittest
import pytest

from launcher.config import parse_config
from launcher.dispatch import Dispatcher


class TestStorageInterface(unittest.TestCase):
    @pytest.mark.only_run_with_direct_target
    def test_dev(self):
        # Remove the output dir
        if os.path.exists("./output/snapshot.db"):
            os.remove("./output/snapshot.db")

        # Parse the config
        config = parse_config("./tests/data/test_config.ini")

        # Run the dispatcher
        dispatcher = Dispatcher(config, dryrun=True)
        new_plates = dispatcher.get_new_directories()
        for plate in new_plates:
            dispatcher.dispatch_plate(plate)

        raise NotImplementedError()
