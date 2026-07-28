import argparse

from lineup_info_collector.crawlers.festivals import get_default_columns, get_default_url
from lineup_info_collector.crawlers.info_crawler import info_crawler
from lineup_info_collector.crawlers.lineup_crawler import lineup_crawler
from lineup_info_collector.exporter.exporter import export_data
from lineup_info_collector.params import CrawlParams


def parse_args() -> argparse.Namespace:
    """Parse the festival/year/url/verbose CLI arguments."""
    parser = argparse.ArgumentParser(description="Collect artists and some info into a CSV.")
    parser.add_argument("-f", "--festival", required=True, help="festival key to crawl, e.g. 'lowlands'.")
    parser.add_argument("-y", "--year", required=True, type=int, help="festival edition year.")
    parser.add_argument("-u", "--url", help="override the festival's default lineup URL.")
    parser.add_argument("-v", "--verbose", action="store_true", help="if set, print verbose.")
    return parser.parse_args()


def main() -> None:
    """Crawl a festival's lineup, enrich it with AllMusic info, and export it to CSV."""
    args = parse_args()
    params = CrawlParams(
        festival=args.festival,
        year=args.year,
        url=args.url or get_default_url(args.festival),
    )

    artists: list[dict[str, str]] = lineup_crawler(params)
    all_artist_info: list[dict[str, str]] = info_crawler(artists, args.verbose)

    export_data(params, all_artist_info, get_default_columns(params.festival))


if __name__ == "__main__":
    main()
