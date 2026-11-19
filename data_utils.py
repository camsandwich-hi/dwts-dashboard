# --------------------------------------------------
# DATA CLEANING UTILITIES
# --------------------------------------------------

# Pandas helps us clean and transform dataset columns.
import pandas as pd


def clean_professional_names(partner_names: pd.Series) -> pd.Series:
    """
    Clean professional dancer names from the DWTS dataset.

    This function:
    1. Removes temporary partner notes in parentheses.
    2. Keeps the primary professional dancer when a slash appears.
    3. Removes extra spaces around names.

    The original dataset column is not modified.
    """

    # Remove notes such as "(Rashad Jennings week 9)".
    cleaned_names = partner_names.str.replace(
        r"\s*\(.*?\)", "", regex=True
    )

    # Keep the first name when multiple partners are separated by "/".
    cleaned_names = cleaned_names.str.split("/").str[0]

    # Remove unnecessary spaces.
    cleaned_names = cleaned_names.str.strip()

    return cleaned_names