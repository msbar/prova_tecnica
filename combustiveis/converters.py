
from datetime import date, datetime


def convert_str_to_float(val):
    try:
        return float(val.replace(',', '.'))
    except:
        return val
