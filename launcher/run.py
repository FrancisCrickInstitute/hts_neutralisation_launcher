import logging
import argparse
from dispatch import Dispatcher
from config import parse_config


def main(config: dict, dryrun: bool, disable_snapshot: bool):
    dispatch = Dispatcher(config, dryrun, disable_snapshot)
    new_plates = dispatch.get_new_directories()
    for plate in new_plates:
        dispatch.dispatch_plate(plate)


if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--dryrun", help="Dry run mode", action="store_true")
    parser.add_argument("--disable_snapshot", help="Disable folder snapshoting", action="store_true")
    args = parser.parse_args()

    # Load config
    if args.config:
        config = parse_config(args.config)
    else:
        config = parse_config()

    # Setup logging
    cfg_analysis = config["analysis"]
    logging.basicConfig(
        filename=cfg_analysis["log_path"],
        level=logging.INFO,
        format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    )

    # Call main
    main(config, args.dryrun, args.disable_snapshot)
