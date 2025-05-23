"""
Tests for util functions
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,no-member

import os

import pytest
from assertpy import assert_that

from launcher.utils import get_experiment_name

class TestUtils:
    @pytest.mark.parametrize(
            "folder_name,expected_exp", 
            [
                ("NAAB10019231__2025-05-16T18_31_04-Measurement 1", "001923"),
                ("NAAB20019231__2025-05-16T18_31_04-Measurement 1", "001923"),
                ("NAAB20019253__2025-05-16T18_31_04-Measurement 2", "001925")
            ]
        )
    def test_get_experiment_name(self, folder_name, expected_exp):
        # Test
        print(folder_name)
        result = get_experiment_name(folder_name)

        # Assert
        assert_that(result).is_equal_to(expected_exp)
