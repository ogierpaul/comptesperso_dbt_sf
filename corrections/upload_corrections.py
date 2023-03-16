import pandas as pd
from stagingfinanzgurutosf import upload_to_table, get_destination

filenames = ['self_cancelling_transactions', 'transaction_id_details']


def read_transaction_id_details(df:pd.DataFrame):
    for c in ['is_transfer', 'scope_out']:
        df[c] = df[c].astype(bool)
    return df


def read_self_cancelling_transactions(df: pd.DataFrame):
    if df['pair_id'].isnull().sum() != 0:
        raise ValueError('pair_id is null, please check transactions')
    if df['transaction_id'].nunique() != df.shape[0]:
        y = df['transaction_id'].value_counts()
        y = y[y > 1]
        y = y.index
        raise ValueError(f'transaction_id is not unique, please check transactions {y}')
    if df['pair_id'].value_counts().any() != 2:
        y = df['pair_id'].value_counts()
        y = y[y != 2]
        y = y.index
        if len(y) > 0:
            raise ValueError(f'pair_id is not unique, please check pairs {y.values}')
    return df

def format_df(fn: str, df:pd.DataFrame) -> pd.DataFrame:
    if fn == 'transaction_id_details':
        df = read_transaction_id_details(df)
    elif fn == 'self_cancelling_transactions':
        df = read_self_cancelling_transactions(df)
    else:
        raise ValueError(f'Unknown filename: {fn}')
    return df

if __name__ == '__main__':
    for fn in filenames:
        df = pd.read_csv(f'{fn}.csv')
        df = format_df(fn, df)
        destination = get_destination(table=fn.upper())
        upload_to_table(df, destination)