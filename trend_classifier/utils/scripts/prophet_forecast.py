import pandas as pd
from utils.functions.prophet_forecasting.get_prophet_weekly_forecast import (
    get_prophet_weekly_forecast,
)
from utils.functions.prophet_forecasting.backtest_mape_last_weeks import (
    backtest_mape_last_weeks,
)
from typing import Tuple


def weekly_volume_forecast_df(
    weekly_volume_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:

    weekly_volume_forecast_df = get_prophet_weekly_forecast(
        weekly_volume_df=weekly_volume_df,
        horizon_weeks=53,
    )

    weekly_volume_only_forecast_df = weekly_volume_forecast_df[
        weekly_volume_forecast_df["ds"] > weekly_volume_df["ds"].max()
    ][["ds", "yhat", "yhat_lower", "yhat_upper"]]

    print(weekly_volume_only_forecast_df)

    weekly_backtest_df, mape = backtest_mape_last_weeks(
        weekly_volume_df=weekly_volume_df
    )

    print("Backtest MAPE (last 8 weeks):", f"{mape:.2%}")
    print(weekly_backtest_df)

    return weekly_volume_only_forecast_df, weekly_backtest_df, mape
