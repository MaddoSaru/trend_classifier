import snowflake.connector
import pandas as pd

from utils.configs.general_configs import USER, PASSWORD, ACCOUNT, WAREHOUSE
from utils.configs.queries_schemas import data_extraction_schema
from utils.functions.data_extraction.fetch_pandas import fetch_pandas
from utils.functions.data_extraction.get_weekly_volume import get_weekly_volume


def get_snowflake_connection():
    return snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
    )


def weekly_volume_df(
    query_path: str,
) -> pd.DataFrame:
    con = get_snowflake_connection()
    cur = con.cursor()

    open_file = open(query_path, "r")
    data_extraction_sql = open_file.read()

    snowflake_data_df = fetch_pandas(
        cur=cur,
        sql=data_extraction_sql,
        field_names=data_extraction_schema,
    )

    weekly_volume_df = get_weekly_volume(
        volume_df=snowflake_data_df,
    )

    return weekly_volume_df
