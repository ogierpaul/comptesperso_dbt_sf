import pandas as pd
import numpy as np
from stagingfinanzgurutosf.src.sf_utils import query_database, get_destination, formatname


def find_umbuchung_for_record(df: pd.DataFrame, r:pd.Series) ->pd.Series:
    def limit_scope_in_time(df, transaction_date, days=31):
        return (abs((df['transaction_date']-transaction_date).dt.days)<= days)
    def find_same_beneficiary(df, beneficiary):
        return (df['beneficiary'] == beneficiary)
    def find_same_amount(df, amount):
        return (df['amount'] == - amount)
    y1 = find_same_amount(df, r['amount'])
    y2 = limit_scope_in_time(df, r['transaction_date'], days=31)
    y3 = find_same_beneficiary(df, r['beneficiary'])
    y_pred = np.all([y1, y2, y3], axis=0)
    y_pred = pd.Series(y_pred, index=df.index)
    possible_matches = df.loc[y_pred]
    if possible_matches.shape[0] > 0:
        possible_matches = possible_matches.sort_values(by=['transaction_date'], ascending=True)
        index_umbuchung = possible_matches.index[0]
    else:
        index_umbuchung = None
    return index_umbuchung

def categorize_umbuchung(df:pd.DataFrame) ->pd.DataFrame:
    out_categories = [
        'OtherAccounts',
        'InternalMovements',
        'Lohn/Gehalt',
        'Kapitalertraege',
        'Elterngeld',
        'Kindergeld',
        'Familiengeld',
        'Verkaufserloes'
    ]
    # possible_positives = df.loc[(df['amount'] >0 ) & (~df['txt_category_lvl3'].isin(out_categories))]
    possible_positives = df.loc[(df['amount'] > 0) & (df['txt_category_lvl3'] == 'InternalMovements')]
    possible_positives['pair_id'] = None
    x = pd.DataFrame(columns = df.columns)
    for i, r_pos in possible_positives.iterrows():
        r_pos = r_pos.copy()
        ix_neg = find_umbuchung_for_record(df, r_pos)
        r_pos['pair_id'] = i
        if ix_neg is not None:
            r_neg = df.loc[ix_neg].copy()
            r_neg['pair_id'] = i
            x = x.append(r_neg)
            x = x.append(r_pos)
    return x

def get_data():
    # table_name='fact_with_corrections'
    # destination = get_destination(table_name, 'DEV_USER1')
    # q = f"""SELECT * \nFROM IDENTIFIER(%s)\n"""
    # df = query_database(q, params=(formatname(destination),))
    # print(df.shape)
    df = pd.read_csv('fact_with_corrections_extract.csv')
    return df

if __name__ == '__main__':
    df = get_data()
    df.columns = [c.lower() for c in df.columns]
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    x = categorize_umbuchung(df)
    x = x[['transaction_id', 'txt_category_lvl3', 'pair_id', 'amount', 'transaction_date', 'beneficiary', 'name_personal_account', 'scope_out'   ]]
    x = x.sort_values(by=['pair_id', 'transaction_date'], ascending=True)
    assert x['transaction_id'].is_unique
    assert round(x['amount'].sum(), 2) == 0.00
    assert x['pair_id'].value_counts().max() == 2
    x.to_csv('self_cancelling_transactions.csv', index=False)
    x = x[['transaction_id', 'pair_id']]
    x.to_csv('self_cancelling_transactions.csv', index=False)