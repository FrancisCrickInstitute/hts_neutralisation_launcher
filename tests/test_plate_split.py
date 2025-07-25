"""
Tests for split_plate functions
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,no-member

import os

import pytest
from assertpy import assert_that

from launcher.plate_split import split_1536_plate

class TestPlateSplit:
    def test_split_1536_plate_full(self, tmp_path):
        # Setup
        dir_path = "tests/data/run_folders/nasal_1536/NAAB10019234__2025-05-16T18_31_04-Measurement 1"

        # Test
        split_1536_plate(dir_path, tmp_path)

        # Extract base plate name
        base_plate = "NAAB10019234"
        measurement = "2025-05-16T18_31_04-Measurement 1"
        expected_workflow_ids = ["001923", "001924", "001925", "001926"]
        expected_dirs = [
            f"{base_plate[:5]}{i}__{measurement}" for i in expected_workflow_ids
        ]

        # Assert
        exist_count = 0
        for output_dir in expected_dirs:
            path = tmp_path / output_dir / "Evaluation1" / "PlateResults.txt"
            assert path.exists(), f"{path} does not exist"
            exist_count += 1

            # Check file content basics
            lines = path.read_text().splitlines()
            assert_that(lines).is_not_empty()

            # Check that some data lines are written
            data_start_index = lines.index("[Data]") + 2  # +1 for header row
            data_rows = lines[data_start_index:]
            assert_that(data_rows).is_not_empty()

            # Check the row count is exactly 384
            assert_that(len(data_rows)).is_equal_to(384)
        
        assert_that(exist_count).is_equal_to(len(expected_dirs)), "Not all expected directories exist"

    def test_split_1536_plate_single(self, tmp_path):
        # Setup
        dir_path = "tests/data/run_folders/nasal_1536/NAAB20019231__2025-05-16T18_31_04-Measurement 2"

        # Test
        split_1536_plate(dir_path, tmp_path)

        # Extract base plate name
        base_plate = "NAAB20019231"
        measurement = "2025-05-16T18_31_04-Measurement 2"
        expected_workflow_ids = ["001923"]
        expected_dirs = [
            f"{base_plate[:5]}{i}__{measurement}" for i in expected_workflow_ids
        ]

        # Assert
        exist_count = 0
        for output_dir in expected_dirs:
            path = tmp_path / output_dir / "Evaluation1" / "PlateResults.txt"
            assert path.exists(), f"{path} does not exist"
            exist_count += 1

            # Check file content basics
            lines = path.read_text().splitlines()
            assert_that(lines).is_not_empty()

            # Check that some data lines are written
            data_start_index = lines.index("[Data]") + 2  # +1 for header row
            data_rows = lines[data_start_index:]
            assert_that(data_rows).is_not_empty()

            # Check the row count is exactly 384
            assert_that(len(data_rows)).is_equal_to(384)
        
        assert_that(exist_count).is_equal_to(len(expected_dirs)), "Not all expected directories exist"


    def test_split_1536_plate_windex(self, tmp_path):
        # Setup
        dir_path = "tests/data/run_folders/nasal_1536/NAAH10019294__250704_161325-V__2025-07-04T17_24_52-Measurement 1"

        # Test
        split_1536_plate(dir_path, tmp_path)

        # Check index file is created
        index_file_path = tmp_path / "NAAH1001932__250704_161325-V2025-07-04T17_24_52-Measurement 1" / "indexfile.txt"
        assert index_file_path.exists(), f"{index_file_path} does not exist"

        # Check file content basics
        lines = index_file_path.read_text().splitlines()
        assert_that(lines).is_not_empty()
