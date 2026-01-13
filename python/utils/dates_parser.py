from datetime import datetime

NAC_FORMAT = "%a %d %b %Y @ %I:%M %p"
UEA_FORMAT = "%d/%m/%Y %H:%M"


def parse_datetime(text, format):
    return datetime.strptime(text, format)

