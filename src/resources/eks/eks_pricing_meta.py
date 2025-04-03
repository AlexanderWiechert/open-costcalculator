from datetime import datetime

RELEASES = {
    "1.27": datetime(2023, 8, 1),
    "1.26": datetime(2023, 4, 1),
    "1.25": datetime(2022, 12, 1),
}

def get_release_date(version):
    return RELEASES.get(version)
