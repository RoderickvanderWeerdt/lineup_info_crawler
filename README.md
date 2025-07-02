# Lineup Info Crawler

A project to crawl festival lineups, gather artist information, and save it to a CSV or return it directly.

## Features

* Crawling festival lineups from web pages.
* Enriching artist data from other sources.
* Exporting data to CSV.
* Providing functions to be used as a library.

## Installation

To set up the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/lineup_info_crawler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd lineup_info_crawler
    ```

3. Install the dependencies using `uv`:

    ```bash
    uv sync
    ```

## Usage

### As a script

You can run the crawler from the command line. Use `uv run main` and specify a festival configuration file from the `params` directory.

```bash
uv run main -- --festival-config params/dtrh_2025.yaml
```

### As a library

You can import and use the functions in your own Python scripts to get lineup data.

```python
from lineup_info_collector.crawlers.lineup_crawler import crawl_lineup
from lineup_info_collector.crawlers.info_crawler import get_artists_info

# Example of getting lineup data for a festival
lineup = crawl_lineup("params/dtrh_2025.yaml")
artists_info = get_artists_info(lineup)

for artist in artists_info:
    print(artist)

```

## Configuration

The `.yaml` files in the `params` directory are used to configure the crawler for different festivals. Each file contains parameters such as the festival name, URL to the lineup page, and CSS selectors to identify artist names on the page.