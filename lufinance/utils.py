
import pandas as _pd
import numpy as _np
import re as _re
import datetime as _datetime

_converter = _re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
def camel_to_snake(s: str) -> str:
    return _converter.sub(r'_\1', s.replace(' ','').replace('%','percent')).lower()

def day_delta(days=0) -> _pd.Timestamp:
    return pdate(_pd.to_datetime('today').date() + _datetime.timedelta(days=days))

def today() -> _pd.Timestamp:
    return pdate(_pd.to_datetime('today'))
def now() -> _pd.Timestamp:
    return pdate(_pd.to_datetime('now'))
def pdate(d) -> _pd.Timestamp:
    return _pd.Timestamp(d)

def mongodate(d) -> str:
    return str(pdate(d).date())

def df(df) -> pd.DataFrame:
    return _pd.DataFrame(df)

def norm_date(d: str) -> str:
    return str(_pd.Timestamp(d).date())


