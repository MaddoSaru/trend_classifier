from utils.scripts.prophet_forecast import weekly_volume_forecast_df
from utils.scripts.data_extraction import weekly_volume_df


weekly_volume_df = weekly_volume_df(
    query_path="utils/queries/data_extraction_query.sql",
)

print(weekly_volume_df.head())

weekly_volume_forecast_df, backtest_df, backtest_mape = weekly_volume_forecast_df(
    weekly_volume_df=weekly_volume_df,
)

print(weekly_volume_forecast_df.head())
print(backtest_df.head())
print(f"Backtest MAPE: {backtest_mape:.2%}")
