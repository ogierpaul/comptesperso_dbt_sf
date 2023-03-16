import pandas as pd

def verify_pairing_internal_movements(df:pd.DataFrame):
    df.columns = [c.lower() for c in df.columns]
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df.sort_values(by=['transaction_date'], inplace=True, ascending=True)
    df = df.loc[df['pair_id'].notnull()]
    y = df.pivot_table(index=['pair_id'], values=['amount'], aggfunc='sum')
    assert y['amount'].abs().max() < 0.01
    for p in df['pair_id'].unique():
        assert df.loc[df['pair_id'] == p, 'amount'].sum() == 0
        assert df.loc[df['pair_id'] == p].shape[0] == 2
        r1 = df.loc[df['pair_id'] == p].iloc[0]
        r2 = df.loc[df['pair_id'] == p].iloc[1]
        if r1['name_personal_account'] != r2['beneficiary']:
            raise Warning(f"""Beneficiary does not match for pair id {p}: {r1['name_personal_account']} != {r2['beneficiary']}""")
    return True

if __name__ == '__main__':
    # df = pd.read_excel('~/Desktop/expenses_paired.xlsx', sheet_name='expenses')
    df = pd.read_csv('self_cancelling_transactions.csv')
    # df.columns = [c.lower() for c in df.columns]
    # df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['transaction_id', 'pair_id']]
    df = df.loc[df['pair_id'].notnull()]
    # previous = pd.read_csv('self_cancelling_transactions.csv')
    # duplicates_pair_ids = df['pair_id'].isin(previous['pair_id']).unique()
    # for p in duplicates_pair_ids:
    #     p_new = previous['pair_id'].max() + p
    #     df.loc[df['pair_id'] == p, 'pair_id'] = p_new
    # df = pd.concat([previous, df], ignore_index=True, axis=0)
    df.to_csv('self_cancelling_transactions.csv', index=False)

