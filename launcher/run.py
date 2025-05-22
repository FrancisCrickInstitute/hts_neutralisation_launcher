import logging
from dispatch import Dispatcher
from config import parse_config

from handlers import HTTPHandler


def main():
    dispatch = Dispatcher()
    new_plates = dispatch.get_new_directories()
    for plate in new_plates:
        dispatch.dispatch_plate(plate)


if __name__ == "__main__":
    cfg_analysis = parse_config()["analysis"]
    logging.basicConfig(
        filename=cfg_analysis["log_path"],
        level=logging.INFO,
        format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    http_handler = HTTPHandler(app="neut_launcher")
    logger.addHandler(http_handler)
    main()
