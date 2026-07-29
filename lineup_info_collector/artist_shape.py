def _check_backup_styles(artist):
    if artist["styles"] == "" or artist["styles"] == ";":
        try:
            artist["styles"] = artist["backup_styles"]
        except:
            print("INFO:", artist["name"], "misses backup styles, but needs one")
    return artist
