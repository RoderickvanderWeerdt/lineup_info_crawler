import argparse
import os

import yaml

from lineup_info_collector.crawlers.info_crawler import info_crawler
from lineup_info_collector.crawlers.lineup_crawler import lineup_crawler
from lineup_info_collector.exporter.exporter import export_data


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
                            It will have 'params' and 'verbose' attributes.
    """
    parser = argparse.ArgumentParser(
        description="Collect artists and some info into a CSV."
    )
    parser.add_argument("-p", "--params", type=str, help="path to the parameters file.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="if set, print verbose."
    )
    args = parser.parse_args()
    return args


def get_params(file: str, verbose: bool) -> dict:
    """Load parameters from a YAML file.

    Args:
        file (str): The path to the YAML parameters file.
        verbose (bool): If True, print the loaded parameters.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If there is an error parsing the YAML file.

    Returns:
        dict: A dictionary containing the parameters from the YAML file.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"Invalid parameters file: {file}")

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
    args: argparse.Namespace = parse_args()

    if not args.params:
        raise ValueError("The --params argument is required.")

    params: dict = get_params(file=args.params, verbose=args.verbose)

    artists: list[dict[str, str]] = lineup_crawler(params)
    all_artist_info: list[dict[str, str]] = info_crawler(artists, args.verbose)

    export_data(params, all_artist_info)


if __name__ == "__main__":
    main()
