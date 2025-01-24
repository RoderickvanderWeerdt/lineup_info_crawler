import os


def export_to_googlesheet(params, all_artist_info):
    raise NotImplementedError
    # Authenticate and connect to Google Sheets
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "google_credentials.json", scope
    )
    client = gspread.authorize(creds)

    # Open the spreadsheet and get the first worksheet
    sheet = client.open(f"{params['FESTIVAL']}_{params['YEAR']}")

    # Get current data to avoid duplicates
    current_data = sheet.get_all_records()

    # Convert current data to a set for quick lookup
    current_artists = {row["name"] for row in current_data}

    # Update the sheet with new data
    for artist in artist_data:
        if artist["name"] not in current_artists:
            sheet.append_row([artist["name"], artist["genre"], artist["styles"]])


def _export_to_csv(params, all_artist_info):
    file_name = f"{params['FESTIVAL']}_{params['YEAR']}.csv"
    filled_acts = []
    if os.path.exists(file_name):
        f = open(file_name, "r")
        for line in f.readlines():
            cols = line.split(",")
            filled_acts.append(cols[0])
        f.close()
        f = open(file_name, "+a")
    else:
        f = open(file_name, "w")

    for artist in all_artist_info:
        if artist["name"] in filled_acts:
            continue
        for col in params["COLUMNS"]:
            f.write(artist[col])
            f.write(",")
        f.write("\n")
    f.close()


def export_data(params, all_artist_info):
    if params["EXPORT_FORMAT"] == "googlesheets":
        return export_to_googlesheet(params, all_artist_info)
    elif params["EXPORT_FORMAT"] == "csv":
        return _export_to_csv(params, all_artist_info)
    else:
        exit(
            f"unknown export format {params['EXPORT_FORMAT']}. Currently accepted are: ['googlesheets', 'csv']"
        )
