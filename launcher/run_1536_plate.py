import logging
from dispatch import Dispatcher
from config import parse_config
from handlers import HTTPHandler
from plate_split import split_1536_plate

cfg_titration = parse_config()["plate_1536"]
RESULTS_DIR = cfg_titration["results_dir"]
SNAPSHOT_DB_PATH = cfg_titration["snapshot_db"]
LOGNAME = cfg_titration["log_path"]


if __name__ == "__main__":
    # Get config 
    cfg_analysis = parse_config()["plate_1536"]

    # Get logger
    logging.basicConfig(
        filename=cfg_analysis["log_path"],
        level=logging.INFO,
        format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    )
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    http_handler = HTTPHandler(app="neut_launcher_1536")
    log.addHandler(http_handler)

    # Find new plates and process them
    dispatch = Dispatcher(results_dir=RESULTS_DIR, db_path=SNAPSHOT_DB_PATH)
    new_plates = dispatch.get_new_directories()
    log.info(f"Found {len(new_plates)} new plates to process.")
    for plate in new_plates:
        log.info(f"Processing plate {plate}.")
        split_1536_plate(plate)
