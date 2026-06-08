from pathlib import Path
import pandas as pd
import argparse


def get_column_names():
    return ['engine_id', 'time'] + [f'operating_setting_{i}' for i in range(1, 4)] + [f'sensor_{i}' for i in range(1, 22)]

def load_data(path: Path) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.
    Args:
        path (Path): The path to the CSV file.
    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    df = pd.read_csv(path, sep=r'\s+', header=None)
    df.columns = get_column_names()
    return df

def add_rul(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Remaining Useful Life (RUL) column to the DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame with engine data.
    Returns:
        pd.DataFrame: The DataFrame with an added RUL column.
    """
    df['RUL'] = df.groupby('engine_id')['time'].transform("max") - df['time']
    return df

def drop_constant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns that have only one unique value.
    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: The DataFrame with constant columns dropped.
    """
    nunique = df.nunique()
    constant_columns = nunique[nunique == 1].index
    df = df.drop(columns=constant_columns)
    return df

def save_data(df: pd.DataFrame, output_path: Path):
    """
    Save the DataFrame to a CSV file.
    Args:
        df (pd.DataFrame): The DataFrame to save.
        path (Path): The path to the output CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "dataset",
        choices=["FD001", "FD002", "FD003", "FD004"],
        help="C-MAPSS dataset to process"
    )

    args = parser.parse_args()

    dataset = args.dataset.upper()

    input_path = Path(
        f"../data/CMAPSSData/train_{dataset}.txt"
    )

    output_path = Path(
        f"../data/processed/{dataset}_processed.csv"
    )

    df = load_data(input_path)
    df = add_rul(df)
    df = drop_constant_columns(df)
    save_data(df, output_path)

if __name__ == "__main__":
    main()