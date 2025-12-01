import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import STL


def extract_features(ts: np.ndarray) -> dict:
    """
    Extract trend and seasonality features from a time series.
    Parameters:
    ts (pd.Series): Time series data with a DateTime index.
    Returns:
    dict: Extracted features including slope, R² values, seasonality strength, and coefficient of variation.
    """

    n = len(ts)
    X = np.arange(n).reshape(-1, 1)
    y = ts.values

    # Linear trend
    lin_reg = LinearRegression().fit(X, y)
    slope = lin_reg.coef_[0]
    r2_linear = lin_reg.score(X, y)

    # Exponential trend
    y_pos = np.where(y <= 0, 1e-6, y)
    log_y = np.log(y_pos)
    exp_reg = LinearRegression().fit(X, log_y)
    exp_growth = exp_reg.coef_[0]
    r2_exponential = exp_reg.score(X, log_y)

    # Seasonality
    try:
        stl = STL(ts, period=12)
        seasonality_strength = 1 - (np.var(stl.resid) / np.var(stl.observed))
    except:
        seasonality_strength = 0

    coeff_var = np.std(y) / (np.mean(y) + 1e-9)

    return {
        "slope": slope,
        "r2_linear": r2_linear,
        "exp_growth": exp_growth,
        "r2_exponential": r2_exponential,
        "seasonality_strength": seasonality_strength,
        "coeff_var": coeff_var,
    }
