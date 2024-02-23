from datetime import datetime


def format_datetime():
    now = datetime.now()
    dt_string = now.strftime("%a, %d %b %Y / %H:%M:%S:%f")
    return dt_string