def auto_label_trend(
    features: dict,
) -> str:
    """
    Auto-label trend based on extracted features.
    Parameters:
    features (dict): Extracted features from the time series.
    Returns:
    str: Auto-labeled trend category.
    """

    slope = features["slope"]
    r2_linear = features["r2_linear"]
    exp_growth = features["exp_growth"]
    r2_exponential = features["r2_exponential"]
    seasonality_strength = features["seasonality_strength"]
    coeff_var = features["coeff_var"]

    # Strong seasonality
    if seasonality_strength > 0.4:
        if slope > 0.1:
            return "Strong Seasonal Upward"
        elif slope < -0.1:
            return "Strong Seasonal Downward"
        else:
            return "Strong Seasonal Flat"

    # Exponential growth
    if r2_exponential > 0.7 and exp_growth > 0.02:
        return "Exponential Growth"

    # Linear
    if r2_linear > 0.6:
        if slope > 0.1:
            return "Linear Upward"
        elif slope < -0.1:
            return "Linear Downward"
        else:
            return "Linear Flat"

    # Irregular / No clear trend
    if coeff_var > 0.3:
        return "Irregular"

    return "Flat"
