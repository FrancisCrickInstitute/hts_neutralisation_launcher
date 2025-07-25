"""
Code for splitting large plates into smaller plates.
"""

import logging
import os
from glob import glob

import pandas as pd

log = logging.getLogger(__name__)

PLATE_384_HEADER = "Row	Column	Plane	Timepoint	Viral Plaques (global) - Area of Viral Plaques Area [µm²] - Mean per Well	Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Mean - Mean per Well	Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) StdDev - Mean per Well	Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Median - Mean per Well	Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Sum - Mean per Well	Cells - Intensity Image Region DAPI (global) Mean - Mean per Well	Cells - Intensity Image Region DAPI (global) StdDev - Mean per Well	Cells - Intensity Image Region DAPI (global) Median - Mean per Well	Cells - Intensity Image Region DAPI (global) Sum - Mean per Well	Cells - Image Region Area [µm²] - Mean per Well	Normalised Plaque area	Normalised Plaque intensity	Number of Analyzed Fields	Global Image Binning	Height [µm]	Time [s]	Compound	Concentration	Cell Type	Cell Count"
PLATE_384_HEADER_LEN = len(PLATE_384_HEADER.split("\t"))
INDEX_FILE_HEADER = "Row	Column	Plane	Timepoint	Sequence	Group	Field	Channel ID	Channel Name	Channel Type	URL	ImageResolutionX [m]	ImageResolutionY [m]	ImageSizeX	ImageSizeY	PositionX [m]	PositionY [m]	Time Stamp	"

def split_1536_plate(dir_path: str, output_dir: str) -> None:
    """
    Split a 1536 well plate into 1-4 384 well plates.
    """

    # Gather information from the directory name
    dir_name = os.path.basename(dir_path)
    plate_name = dir_name.split("__")[0]
    measurement_name = ''.join(dir_name.split("__")[1:])
    exp_type = plate_name[0]
    virus_id = plate_name[1:4]
    rep_num = plate_name[4]
    workflow_id = plate_name[-7:-1]
    number_of_plates = int(plate_name[-1])

    # Log the information
    log.info(f"Splitting {dir_name} into {number_of_plates} plates.")
    log.info(f"Plate name: {plate_name}")
    log.info(f"Measurement name: {measurement_name}")
    log.info(f"Experiment type: {exp_type}")
    log.info(f"Virus ID: {virus_id}")
    log.info(f"Replicate number: {rep_num}")
    log.info(f"Workflow ID: {workflow_id}")
    log.info(f"Number of plates: {number_of_plates}")

    # Load the plate mapping
    plate_mapping = load_plate_mapping()

    # Load the 1536 plate results
    path = os.path.join(dir_path, "Evaluation*", "PlateResults.txt")
    log.info(f"Loading plate results from {path}")
    all_evaluations = glob(os.path.join(dir_path, "Evaluation*", "PlateResults.txt"))
    if len(all_evaluations) > 1:
        logging.warning("multiple Evaluation directories found, using the latest")
    plate_result_path = sorted(all_evaluations)[-1]

    # Load plate header, read first 8 lines
    plate_header = []
    with open(plate_result_path, "r") as file:
        for _ in range(6):
            line = file.readline().strip()
            plate_header.append(line)

    # Load source plate data
    # 0 Row                                    3
    # 1 Column                                 46
    # 2 Plane                                  1
    # 3 Timepoint                              1
    # 4 Nuclei Selected - Number of Objects    1912
    # 5 Infected cell - Number of Objects      1339
    # 6 Percentage infected                     0.700314
    # 7 Number of Analyzed Fields               1
    # 8 Height [µm]                             0
    # 9 Time [s]                                0
    # 10 Compound                               NaN
    # 11 Concentration                          NaN
    # 12 Cell Type                              NaN
    # 13 Cell Count                             NaN
    source_df = pd.read_csv(
        plate_result_path,
        skiprows=8,
        sep="\t",
        skip_blank_lines=True,
        na_values=["", "NA"],
    )
    source_df = source_df.fillna(0)

    # Cast to strict dtypes
    source_df = source_df.astype({
        "Row": "int32",
        "Column": "int32",
        "Plane": "int32",
        "Timepoint": "int32",
        "Nuclei Selected - Number of Objects": "int32",
        "Infected cell - Number of Objects": "int32",
        "Percentage infected": "float64",
        "Number of Analyzed Fields": "int32",
        "Height [µm]": "float64",
        "Time [s]": "int32",
    })

    # Check for index file and load
    index_file_path = os.path.join(dir_path, "indexfile.txt")
    index_df = None
    if os.path.exists(index_file_path):
        log.info(f"Index file found: {index_file_path}")

        # Check if the index file is empty
        if os.path.getsize(index_file_path) != 0:
            # Load the index file
            index_df = pd.read_csv(
                index_file_path,
                sep="\t",
                skip_blank_lines=True,
                na_values=["", "NA"],
                dtype=str,
            )
            index_df = index_df.fillna(0)
            index_df = index_df.loc[:, ~index_df.columns.str.contains('^Unnamed')]
        else:
            log.warning(f"Index file is empty: {index_file_path}")

    # Cycle the plates and create output files
    for i in range(number_of_plates):
        plate_num = i + 1
        new_workflowid = str(int(workflow_id) + i).zfill(len(workflow_id))
        log.info(f"Processing plate {i+1} of {number_of_plates}")
        log.info(f"New workflow ID: {new_workflowid}")

        # Create the new plate name and dir
        new_plate_name = exp_type + virus_id + rep_num + new_workflowid
        new_output_dir = new_plate_name + "__" + measurement_name
        log.info(f"New output dir: {new_output_dir}")
        plate_output_path = os.path.join(output_dir, new_output_dir)

        # Create the new output directory structure
        os.makedirs(plate_output_path, exist_ok=True)
        os.makedirs(os.path.join(plate_output_path, "Evaluation1"), exist_ok=True)

        # Create the new plate results file
        plate_result_path = os.path.join(plate_output_path, "Evaluation1", "PlateResults.txt")
        with open(plate_result_path, "w") as file:
            # Write the header
            for line in plate_header:
                file.write(line + "\n")
            file.write("\n")
            file.write("[Data]\n")
            file.write(PLATE_384_HEADER + "\n")

            # Write the data
            for row in source_df.itertuples(index=False):
                # Get 384 well mapping
                well_id = str(row[0]) + ":" + str(row[1])
                mapping_384 = plate_mapping[well_id]

                # Check if the mapping is for this plate
                if int(mapping_384[2]) != plate_num:
                    continue

                # Fill a row array with blanks for length of 384 well plate
                new_row = [""] * PLATE_384_HEADER_LEN

                # Fill in data - expanded for easier reading
                new_row[0] = mapping_384[0]  # Row
                new_row[1] = mapping_384[1]  # Column
                new_row[2] = row[2]          # Plane
                new_row[3] = row[3]          # Timepoint
                new_row[4] = row[5]          # Viral Plaques (global) - Area of Viral Plaques Area [µm²] - Mean per Well <- Infected cell - Number of Objects
                new_row[5] = ""              # Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Mean - Mean per Well
                new_row[6] = ""              # Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) StdDev - Mean per Well
                new_row[7] = ""              # Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Median - Mean per Well
                new_row[8] = ""              # Viral Plaques (global) - Intensity Viral Plaques Alexa 488 (global) Sum - Mean per Well
                new_row[9] = ""              # Cells - Intensity Image Region DAPI (global) Mean - Mean per Well
                new_row[10] = ""             # Cells - Intensity Image Region DAPI (global) StdDev - Mean per Well
                new_row[11] = ""             # Cells - Intensity Image Region DAPI (global) Median - Mean per Well
                new_row[12] = ""             # Cells - Intensity Image Region DAPI (global) Sum - Mean per Well
                new_row[13] = row[4]         # Cells - Image Region Area [µm²] - Mean per Well <- Nuclei Selected - Number of Objects
                new_row[14] = row[6]         # Normalised Plaque area <- Percentage infected
                new_row[15] = ""             # Normalised Plaque intensity
                new_row[16] = row[7]         # Number of Analyzed Fields
                new_row[17] = ""             # Global Image Binning
                new_row[18] = row[8]         # Height [µm]
                new_row[19] = row[9]         # Time [s]
                new_row[20] = ""             # Compound
                new_row[21] = ""             # Concentration
                new_row[22] = ""             # Cell Type
                new_row[23] = ""             # Cell Count

                # Write the row to the file
                file.write("\t".join([str(x) for x in new_row]) + "\n")

        if index_df is not None:
            index_output_path = os.path.join(plate_output_path, "indexfile.txt")
            log.info(f"Writing index file to {index_output_path}")
            with open(index_output_path, "w") as file:
                file.write(INDEX_FILE_HEADER + "\n")

                # Write the data
                for row in index_df.itertuples(index=False):
                    # Get 384 well mapping
                    well_id = row[0] + ":" + row[1]
                    mapping_384 = plate_mapping[well_id]

                    # Check if the mapping is for this plate
                    if int(mapping_384[2]) != plate_num:
                        continue

                    # Covert data row to tab separated string
                    new_row = [
                        mapping_384[0],  # Row
                        mapping_384[1],  # Column
                        row[2],          # Plane
                        row[3],          # Timepoint
                        row[4],          # Sequence
                        row[5],          # Group
                        row[6],          # Field
                        row[7],          # Channel ID
                        row[8],          # Channel Name
                        row[9],          # Channel Type
                        row[10],         # URL
                        row[11],         # ImageResolutionX [m]
                        row[12],         # ImageResolutionY [m]
                        row[13],         # ImageSizeX
                        row[14],         # ImageSizeY
                        row[15],         # PositionX [m]
                        row[16],         # PositionY [m]
                        row[17]          # Time Stamp
                    ]
                    file.write("\t".join([str(x) for x in new_row]) + "\t\n")

        log.info(f"Plate results written to {plate_result_path}")

def load_plate_mapping() -> dict:
    """
    Load the plate mapping from the config file.
    """

    # Load plate mapping from file
    plate_mapping = {}
    count  = 0
    with open("launcher/data/1536to4x384.csv", "r") as file:
        for line in file:
            # Skip first line
            count += 1
            if count == 1:
                continue

            # Grab the line data
            line = line.strip()
            line_split = line.split(",")
            id = line_split[0] + ":" + line_split[1]
            plate_mapping[id] = [line_split[3], line_split[4], line_split[2]]

    return plate_mapping