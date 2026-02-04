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
        try:
            params: dict = yaml.safe_load(f)
            if verbose:
                print(f"Parameters from file {file}")
                print(params)
            return params
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {file}") from e


def main() -> None:
    """Main function to run the data collection and export process.

    This function orchestrates the entire process. It parses command-line
    arguments to get the parameters file, loads the parameters, crawls the
    lineup to get a list of artists, fetches additional information for
    each artist, and finally exports all the collected data.
    """
    
    # args: argparse.Namespace = parse_args()

    # if not args.params:
    #     raise ValueError("The --params argument is required.")

    # params: dict = get_params(file=args.params, verbose=args.verbose)

    # params = get_params(file="params/lowlands_2025.yaml", verbose=True)
    # params = get_params(file="params/dtrh_2025.yaml", verbose=True)
    # params = get_params(file="params/pinkpop_2025.yaml", verbose=False)
    # params = get_params(file="params/dtrh_2025.yaml", verbose=True)
    params = get_params(file="params/pinkpop_2026.yaml", verbose=True)
    # params = get_params(file="params/bks_2026.yaml", verbose=True)
    # params = get_params(file="params/ooto_2025.yaml", verbose=False)
    # params = get_params(file="params/prettypissed_2025.yaml", verbose=False)
    


    artists: list[dict[str, str]] = lineup_crawler(params)
    all_artist_info: list[dict[str, str]] = info_crawler(artists, True)

    export_data(params, all_artist_info)


if __name__ == "__main__":
    main()
