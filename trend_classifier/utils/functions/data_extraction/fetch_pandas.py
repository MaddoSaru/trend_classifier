import pandas as pd
from typing import List


def fetch_pandas(cur, sql: str, field_names: List):
    cur.execute(sql)
    rows = 0
    while True:
        data = cur.fetchmany(5000000)
        if not data:
            break
        df = pd.DataFrame(data, columns=cur.description)
        rows += df.shape[0]
    if rows == 0:
        df = pd.DataFrame(columns=field_names)
    else:
        df.columns = field_names
    return df
