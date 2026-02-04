import os


# def export_to_googlesheet(
#     params: dict[str, str | int | list[str]], all_artist_info: list[dict[str, str]]
# ) -> None:
#     """Exports artist information to a Google Sheet.

#     Note: This function is not yet implemented.

#     Args:
#         params (dict[str, str | int | list[str]]): A dictionary of parameters, including Google Sheets details.
#         all_artist_info (list[dict[str, str]]): A list of dictionaries, where each dictionary contains
#                                                 information about an artist.
#     """
#     raise NotImplementedError


def _check_backup_styles(artist):
    if artist["styles"] == "" or artist["styles"] == ";":
        try:
            artist["styles"] = artist["backup_styles"]
        except:
            print("INFO:", artist["name"], "misses backup styles, but needs one")
    return artist


# def _export_to_csv(
#     params: dict[str, str | int | list[str]], all_artist_info: list[dict[str, str]]
# ) -> None:
def _export_to_csv(params, all_artist_info):
    """Exports artist information to a CSV file.

    The CSV file is named based on the festival and year specified in the parameters.
    It appends new artists to the file if it already exists, avoiding duplicate entries.

    Args:
        params (dict[str, str | int | list[str]]): A dictionary of parameters, including 'FESTIVAL', 'YEAR',
                                                    and 'COLUMNS'.
        all_artist_info (list[dict[str, str]]): A list of dictionaries, where each dictionary contains
                                                information about an artist.
    """
    if not all_artist_info:
        print("No artist information to export.")
        return

    file_name: str = f"{params.get('FESTIVAL', '')}_{params.get('YEAR', '')}.csv"
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
                if params["FESTIVAL"] == "lowlands" or params['FESTIVAL']=="BKS":
                    artist = _check_backup_styles(artist)
                artist["name"] = artist["name"].replace(",", ";")
                if artist.get("name") in filled_acts:
                    continue
                try:
                    row_data: list[str] = []
                    columns = params.get("COLUMNS", []) #are we assuming a different set of columns for each row?
                    if not isinstance(columns, list):
                        print(
                            "Warning: 'COLUMNS' parameter is not a list, skipping row."
                        )
                        continue
                    for col in columns:
                        value = artist.get(col, "")
                        row_data.append(str(value).replace(",", ";"))
                    f.write(",".join(row_data) + "\n")
                except KeyError as e:
                    print(f"Skipping artist due to missing key: {e}")

    except (IOError, PermissionError) as e:
        raise IOError(f"Error writing to file {file_name}: {e}") from e


# def export_data(
#     params: dict[str, str | int | list[str]], all_artist_info: list[dict[str, str]]
# ) -> None:
def export_data(params, all_artist_info):
    """Exports data to the specified format.

    This function acts as a dispatcher, calling the appropriate export function
    based on the 'EXPORT_FORMAT' parameter.

    Args:
        params (dict[str, str | int | list[str]]): A dictionary of parameters, including 'EXPORT_FORMAT'.
        all_artist_info (list[dict[str, str]]): A list of dictionaries, where each dictionary contains
                                                information about an artist.

    Raises:
        ValueError: If the 'EXPORT_FORMAT' is invalid or not specified.
    """
    export_format = params.get("EXPORT_FORMAT")
    if not isinstance(export_format, str):
        raise ValueError(f"Invalid or missing EXPORT_FORMAT in params: {export_format}")

    if export_format == "googlesheets":
        export_to_googlesheet(params, all_artist_info)
    elif export_format == "csv":
        _export_to_csv(params, all_artist_info)
    else:
        exit(
            f"unknown export format {params['EXPORT_FORMAT']}. Currently accepted are: ['googlesheets', 'csv']"
        )
