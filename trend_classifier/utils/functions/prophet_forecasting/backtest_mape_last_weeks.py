import pandas as pd
from prophet import Prophet
from typing import Optional


def backtest_mape_last_weeks(
    weekly_volume_df: pd.DataFrame, n_holdoutput: Optional[int] = 8, **fit_kwargs
):

    if len(weekly_volume_df) <= n_holdoutput:
        raise ValueError("Not enough history to backtest that many weeks.")

    train = weekly_volume_df.iloc[:-n_holdoutput].copy()
    test = weekly_volume_df.iloc[-n_holdoutput:].copy()

    m = Prophet(
        weekly_seasonality=True,
        yearly_seasonality=True,
        daily_seasonality=False,
        **fit_kwargs
    )
    m.add_regressor("active_brands")
    m.fit(train[["ds", "y", "active_brands"]])

    future = test[["ds", "active_brands"]].copy()
    forecast = m.predict(future)[["ds", "yhat"]]
    output = test.merge(forecast, on="ds", how="left")

    output["abs_pct_err"] = (output["y"] - output["yhat"]).abs() / output["y"].clip(
        lower=1e-9
    )
    mape = output["abs_pct_err"].mean()
    return output, mape
