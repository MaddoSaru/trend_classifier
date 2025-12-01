import pandas as pd
from prophet import Prophet
from typing import Optional, Union


def get_prophet_weekly_forecast(
    weekly_volume_df: pd.DataFrame,
    horizon_weeks: Optional[int] = 8,
    add_extra_quarterly_seasonality: Optional[bool] = True,
    changepoint_prior_scale: Optional[float] = 0.05,
    week_ending: Optional[str] = "SAT",
    future_active_brands: Optional[Union[pd.Series, dict]] = None,
) -> pd.DataFrame:

    m = Prophet(
        weekly_seasonality=True,
        yearly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=changepoint_prior_scale,
    )
    m.add_regressor("active_brands")

    if add_extra_quarterly_seasonality:
        m.add_seasonality(name="quarterly_like", period=13, fourier_order=5)

    m.fit(weekly_volume_df[["ds", "y", "active_brands"]])

    week_alias = {
        "SUN": "W-SUN",
        "MON": "W-MON",
        "TUE": "W-TUE",
        "WED": "W-WED",
        "THU": "W-THU",
        "FRI": "W-FRI",
        "SAT": "W-SAT",
    }[week_ending.upper()]

    future = m.make_future_dataframe(periods=horizon_weeks, freq=week_alias)

    future = future.merge(
        weekly_volume_df[["ds", "active_brands"]], on="ds", how="left"
    )

    last_ab = weekly_volume_df["active_brands"].iloc[-1] if len(weekly_volume_df) else 0

    if future_active_brands is not None:

        if isinstance(future_active_brands, dict):
            future_active_brands = pd.Series(future_active_brands)
            future_active_brands.index = pd.to_datetime(future_active_brands.index)
        else:
            future_active_brands = future_active_brands.copy()

            if future_active_brands.index.name != "ds":
                future_active_brands.index = pd.to_datetime(future_active_brands.index)

        mask_future = future["active_brands"].isna()
        future.loc[mask_future, "active_brands"] = future.loc[mask_future, "ds"].map(
            future_active_brands
        )
        future["active_brands"] = future["active_brands"].fillna(last_ab)
    else:

        future["active_brands"] = future["active_brands"].fillna(last_ab)

    forecast = m.predict(future)

    for col in ["yhat", "yhat_lower", "yhat_upper"]:
        forecast[col] = forecast[col].clip(lower=0)

    return forecast
