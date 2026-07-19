"""
Serialization utilities.

Converts NumPy and Pandas objects into native Python
types that can be safely returned through MCP/JSON.
"""

import numpy as np
import pandas as pd


def to_python(obj):
    """
    Recursively convert objects into JSON-friendly types.
    """

    if isinstance(obj, dict):
        return {k: to_python(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [to_python(v) for v in obj]

    if isinstance(obj, tuple):
        return tuple(to_python(v) for v in obj)

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")

    if isinstance(obj, pd.Series):
        return obj.to_dict()

    return obj