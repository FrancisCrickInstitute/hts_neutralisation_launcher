#!/bin/env python

import argparse
import sqlalchemy
import sqlite3


def parse_workflow_ids(workflow_ids):
    """add zero padding and convert to string for database query"""
    if isinstance(workflow_ids, int):
        return f"{workflow_ids:06}"
    elif isinstance(workflow_ids, list):
        return [f"{i:06}" for i in workflow_ids]
    else:
        raise TypeError


def create_connection():
    con = sqlalchemy.create_engine(
        "sqlite:///processed_experiments.sqlite"
    )
    return con


def remove_processed(workflow_ids):
    """docstring"""
    con = create_connection()
    con.execute(
        "DELETE FROM processed WHERE experiment IN (%s)" %
        ",".join("?" * len(workflow_ids)),
        workflow_ids
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove entries from sqlite database"
    )
    parser.add_argument(
        "workflow_ids",
        metavar="N",
        type=int,
        nargs="+",
        help="workflow IDs to remove"
    )
    parser.add_argument(
        "-v",
        "--variant",
        nargs="*",
        default=["a", "b", "c"],
        help="variants to remove"
    )
    args = parser.parse_args()

    workflow_ids = parse_workflow_ids(args.workflow_ids)
    print(f"--- Removing: {workflow_ids} variants: {args.variant} from: processed ---")
    remove_processed(workflow_ids)
