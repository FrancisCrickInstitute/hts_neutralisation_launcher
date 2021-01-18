import os
import logging
import sqlite3
import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

import task


class MyEventHandler(LoggingEventHandler):

    def __init__(self, input_dir, db_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_dir = input_dir
        self.db_path = db_path
        self.create_db()

    def on_created(self, event):
        """
        over-ride method when file or directory is created
        """
        super().on_created(event)
        src_path = event.src_path
        experiment = self.get_experiment_name(src_path)
        if experiment is None:
            # invalid experiment name, skip
            return None
        if self.experiment_exists(experiment):
            logging.info(
                f"experiment {experiment} already exists in processed database"
            )
        else:
            logging.info(f"new experiment: {experiment}")
            logging.info("creating plate_list")
            plate_list = self.create_plate_list(experiment)
            if len(plate_list) == 8:
                logging.info("launching analysis job")
                task.background_analysis.delay(plate_list)
                logging.info("analysis complete, adding to processed database")
                self.add_experiment_to_db(experiment)
            else:
                logging.error(
                    f"plate list length = {len(plate_list)} expected 8"
                )

    def create_plate_list(self, experiment):
        """
        create a plate list from an experiment name
        """
        all_subdirs = [i for i in os.listdir(self.input_dir)]
        full_paths = [os.path.join(self.input_dir, i) for i in all_subdirs]
        # filter to just those of the specific experiment
        wanted_experiment = []
        for i in full_paths:
            final_path = i.split(os.sep)[-1]
            if final_path[3:9] == experiment:
                wanted_experiment.append(i)
        return wanted_experiment

    def get_experiment_name(self, dir_name):
        """
        get the name of the experiment from a plate directory
        """
        plate_dir = dir_name.split(os.sep)[-1]
        if plate_dir.startswith("A"):
            return plate_dir.split("__")[0][-6:]
        else:
            logging.error(
                f"invalid plate directory name {plate_dir}, skipping"
            )

    def experiment_exists(self, experiment):
        """
        check if an experiment is already in the processed database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM processed WHERE experiment=(?))",
            (experiment, )
        )
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists

    def add_experiment_to_db(self, experiment):
        """add an experiment to the processed database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO processed (experiment) VALUES (?);",
            (experiment, )
        )
        conn.commit()
        cursor.close()

    def create_db(self):
        """
        create processed experiments database if it doesn't
        already exist
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processed
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment CHAR(10) NOT NULL
            );
            """
        )
        conn.commit()
        cursor.close()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = "/usr/src/app/testdir"
    db_path = "/usr/src/app/processed_experiments.sqlite"

    event_handler = MyEventHandler(path, db_path)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

