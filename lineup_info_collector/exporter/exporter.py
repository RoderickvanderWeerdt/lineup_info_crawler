import os

from lineup_info_collector.params import CrawlParams


def _check_backup_styles(artist):
    if artist["styles"] == "" or artist["styles"] == ";":
        try:
            artist["styles"] = artist["backup_styles"]
        except:
            print("INFO:", artist["name"], "misses backup styles, but needs one")
    return artist


def _export_to_csv(params: CrawlParams, all_artist_info: list[dict], columns: list[str]) -> None:
    """Exports artist information to a CSV file.

    The CSV file is named based on the festival and year specified in the parameters.
    It appends new artists to the file if it already exists, avoiding duplicate entries.

    Args:
        params: The festival/year/url this crawl was run for.
        all_artist_info: A list of dictionaries, where each dictionary contains
            information about an artist.
        columns: The artist dict keys to write out as CSV columns, in order.
    """
    if not all_artist_info:
        print("No artist information to export.")
        return

    file_name: str = f"{params.festival}_{params.year}.csv"
    filled_acts: list[str] = []

    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                for line in f:
                    cols = line.strip().split(",")
                    if cols:
                        filled_acts.append(cols[0])

        with open(file_name, "a+") as f:
            for artist in all_artist_info:
                if params.festival in ("lowlands", "bks"):
                    artist = _check_backup_styles(artist)
                artist["name"] = artist["name"].replace(",", ";")
                if artist.get("name") in filled_acts:
                    continue
                try:
                    row_data: list[str] = []
                    for col in columns:
                        value = artist.get(col, "")
                        row_data.append(str(value).replace(",", ";"))
                    f.write(",".join(row_data) + "\n")
                except KeyError as e:
                    print(f"Skipping artist due to missing key: {e}")

    except (IOError, PermissionError) as e:
        raise IOError(f"Error writing to file {file_name}: {e}") from e


def export_data(params: CrawlParams, all_artist_info: list[dict], columns: list[str]) -> None:
    """Exports artist information to CSV."""
    _export_to_csv(params, all_artist_info, columns)
