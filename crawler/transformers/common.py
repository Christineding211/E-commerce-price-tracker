import re
from typing import Any
import pandas as pd

def clean_price(value: Any) -> int | None:
    """Convert price inputs like '$1,299' or 1299 into integers. Return None if unparseable."""
    # 1. Check for null/missing values
    if value is None or pd.isna(value):
        return None

    # 2. Convert to string and strip 
    text = str(value).strip()

    # 3. Remove non-numeric characters except decimal points (e.g., currency symbols, commas)
    # Example: converts "$1,299" to "1299"
    cleaned_text = re.sub(r"[^\d.]", "", text)

    # 4.  convert to an integer
    try:
        # float("1299.00") -> 1299.0 -> int(1299.0) -> 1299
        return int(float(cleaned_text))
    except (ValueError, TypeError):
        # Return None if conversion fails (e.g., empty string or invalid input)
        return None
    