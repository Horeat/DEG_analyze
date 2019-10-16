import pandas as pd
from .view import file_in,control_in,case_in   #????????

def IsColumnExist():
    c = file_in.columns.values.tolist()
    if control_in in c:
        if case_in in c:
            return "Both columns are valid. Please proceed to the next step!"
        else:
            return "Case column is not exist. Please check or reload file!"
    else:
        if case_in in c:
            return "Control column is not exist. Please check or reload file!"
        else:
            return "Both columns are not exist. Please check or reload file!"


def SelectDeg(gev_in,pv_in):
    filtered = None
    filtered = file_in[(abs(file_in['A']-file_in['B']) > 1) & (file_in['p_value'] < 0.05)]
    return filtered


