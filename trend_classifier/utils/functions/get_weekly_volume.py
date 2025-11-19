import pandas as pd
from typing import Optional


def get_weekly_volume(
    volume_df: pd.DataFrame,
    date_field: Optional[str] = "RECEIVED_AT_ORIGIN_PROCESSING_DATE_UTC",
    volume_field: Optional[str] = "SHIPMENT_VOLUME",
    brand_field: Optional[str] = "BRAND_NAME",
    week_ending: Optional[str] = "SAT",
    exclude_partial_current_week: Optional[bool] = True,
) -> pd.DataFrame:

    week_alias = {
        "SUN": "W-SUN",
        "MON": "W-MON",
        "TUE": "W-TUE",
        "WED": "W-WED",
        "THU": "W-THU",
        "FRI": "W-FRI",
        "SAT": "W-SAT",
    }[week_ending.upper()]

    volume_df[date_field] = pd.to_datetime(volume_df[date_field])

    grouped_df = (
        volume_df.set_index(date_field)
        .resample(week_alias)
        .agg(
            **{
                "y": (volume_field, "sum"),
                "active_brands": (brand_field, "nunique"),
            }
        )
        .reset_index()
        .rename(columns={date_field: "ds"})
    )

    aggregated_volume_df = grouped_df.copy()

    if exclude_partial_current_week and not aggregated_volume_df.empty:
        last_week_end = aggregated_volume_df["ds"].max()
        if last_week_end > pd.Timestamp.today().normalize():
            aggregated_volume_df = aggregated_volume_df.iloc[:-1]

    aggregated_volume_df["y"] = aggregated_volume_df["y"].clip(lower=0)
    aggregated_volume_df["active_brands"] = (
        aggregated_volume_df["active_brands"].fillna(0).astype(int)
    )

    return aggregated_volume_df
