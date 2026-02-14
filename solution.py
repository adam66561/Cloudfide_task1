import pandas as pd 
import re

OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}

LABEL_PATTERN = re.compile(r"^[A-Za-z_]+$")
def validate_labels_role(col1, op, col2, new_column) -> bool:
    return (
        op in OPS
        and bool(LABEL_PATTERN.match(col1))
        and bool(LABEL_PATTERN.match(col2))
        and bool(LABEL_PATTERN.match(new_column))
    )

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Adds a new virtual column to a DataFrame based on a simple arithmetic expression.

    The role must be in the form: "<column> <operator> <column>",
    where operator is one of: +, -, *.
    Column names must contain only letters and underscores.

    Returns a new DataFrame with the additional column.
    Returns an empty DataFrame if validation fails. 
    """

    df_copy = df.copy()

    if not isinstance(role, str) or not isinstance(new_column, str):
        return pd.DataFrame()
    
    parts = re.split(r"\s*([+\-*])\s*", role.strip())
    if len(parts) != 3:
        return pd.DataFrame()
    col1, op, col2 = parts

    if not validate_labels_role(col1, op, col2, new_column):
        return pd.DataFrame()
    
    if col1 not in df_copy.columns or col2 not in df_copy.columns:
        return pd.DataFrame()
    
    df_copy[new_column] = OPS[op](df_copy[col1], df_copy[col2])
    
    return df_copy