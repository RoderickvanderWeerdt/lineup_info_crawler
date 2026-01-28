import argparse
import os

import yaml

from lineup_info_collector.crawlers.info_crawler import info_crawler
from lineup_info_collector.crawlers.lineup_crawler import lineup_crawler
from lineup_info_collector.exporter.exporter import export_data


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect artists and some info into a CSV."
    )
    parser.add_argument("-p", "--params", type=str, help="path to the parameters file.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="if set, print verbose."
    )
    args = parser.parse_args()
    return args


def get_params(file: str, verbose: bool):
    if not os.path.exists(file):
        exit(f"Invalid parameters file {file}.")

    with open(file, "r") as f:
        params = yaml.safe_load(f)
        if verbose:
            print(f"Parameters from file {file}")
            print(params)
    return params


def main():
    try:
        args = parse_args()
        params = get_params(file=args.params, verbose=args.verbose)
    except:
        # params = get_params(file="params/lowlands_2025.yaml", verbose=True)
        # params = get_params(file="params/dtrh_2025.yaml", verbose=True)
        # params = get_params(file="params/pinkpop_2025.yaml", verbose=False)
        params = get_params(file="params/bks_2026.yaml", verbose=True)
        # params = get_params(file="params/pinkpop_2026.yaml", verbose=True)
        # params = get_params(file="params/ooto_2025.yaml", verbose=False)
        # params = get_params(file="params/prettypissed_2025.yaml", verbose=False)
    
    artists = lineup_crawler(params)
    print("Finished with Line-up crawling, starting Info Crawling...")
    all_artist_info = info_crawler(artists, args.verbose)

    export_data(params, all_artist_info)


if __name__ == "__main__":
    main()
