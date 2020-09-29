import sys
import argparse
import numpy as np
import pandas as pd


def parse_args(args):
    """
    Parse the command line arguments: number of rows and columns for random table
    and table type.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        choices={"flat", "square"},
        help="The table format: either 'flat' or 'square'")
    parser.add_argument("filename", help="What to call the file.")
    parser.add_argument(
        "-d", "--days",
        type=int,
        help="The number of days for which to generate data.",
        required=False,
        default=365
    )
    return parser.parse_args()


def generate_pandas_table(n_days, table_type):
    """
    Returns a Pandas DataFrame generated from the given parameters.
    """
    if table_type == "flat":
        table = generate_flat_table(n_days)
    elif table_type == "square":
        table = generate_square_table(n_days)
    else:
        raise ValueError(f"Unexpected table type {table_type}")
    return table


def generate_flat_table(n_days):
    """
    Generates a flat table of data for the number of days given.
    """
    index = generate_flat_index(n_days)
    data = np.round(np.random.rand(n_days*48) * 100, 2)
    df = pd.DataFrame(index=index, data=data)
    df.index.name = 'HH'
    return df

def generate_square_table(n_days):
    index = generate_square_index(n_days)
    data = np.round(np.random.rand(n_days, 48) * 100, 2)
    df = pd.DataFrame(
        index=index,
        columns=["HH%i" % i for i in range(48)],
        data=data
    )
    df.index.name = 'D'
    return df


def generate_flat_index(n_days):
    """
    Returns an index of HH data stacked in a 1D vector
    """
    return pd.date_range(
        start="2020-01-01 00:00:00",
        periods=n_days*48,
        freq="30T"
    )


def generate_square_index(n_days):
    return pd.date_range(
        start="2020-01-01 00:00:00",
        periods=n_days,
        freq="D"
    )

def write_table(filename, df):
    if get_extension(filename) in ['xls', 'xlsx']:
        df.to_excel(filename)
    else:
        df.to_csv(filename)


def get_extension(filename):
    """
    return the extension given in the filename
    """
    return filename.split('.')[-1]


if __name__ == "__main__":
    args = parse_args(sys.argv)
    table = generate_pandas_table(args.days, args.type)
    write_table(args.filename, table)
    
