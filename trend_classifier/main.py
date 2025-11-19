import snowflake.connector

from utils.configs.general_configs import USER, PASSWORD, ACCOUNT, WAREHOUSE
from utils.configs.queries_schemas import data_extraction_schema
from utils.functions.fetch_pandas import fetch_pandas
from utils.functions.get_weekly_volume import get_weekly_volume
from utils.functions.get_prophet_weekly_forecast import get_prophet_weekly_forecast
from utils.functions.backtest_mape_last_weeks import backtest_mape_last_weeks


def get_snowflake_connection():
    return snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
    )


con = get_snowflake_connection()
cur = con.cursor()

open_file = open(f"utils/queries/data_extraction_query.sql", "r")
data_extraction_sql = open_file.read()

snowflake_data_df = fetch_pandas(
    cur=cur,
    sql=data_extraction_sql,
    field_names=data_extraction_schema,
)

weekly_volume_df = get_weekly_volume(
    volume_df=snowflake_data_df,
)

print(weekly_volume_df.head())

weekly_volume_forecast_df = get_prophet_weekly_forecast(
    weekly_volume_df=weekly_volume_df,
    horizon_weeks=53,
)


weekly_volume_only_forecast_df = weekly_volume_forecast_df[
    weekly_volume_forecast_df["ds"] > weekly_volume_df["ds"].max()
][["ds", "yhat", "yhat_lower", "yhat_upper"]]

print(weekly_volume_only_forecast_df)

bt, mape = backtest_mape_last_weeks(weekly_volume_df=weekly_volume_df)

print("Backtest MAPE (last 8 weeks):", f"{mape:.2%}")
print(bt)
