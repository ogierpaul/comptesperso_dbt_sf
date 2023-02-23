import pandas as pd
import yaml
import os

def load_yaml(fn:str) ->dict:
    with open(fn) as f:
        d = yaml.safe_load(f)
    return d

def load_dict_to_level_based_hierarchy(d:dict) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(d, orient='index')
    df.index.name = 'L0'
    df = pd.melt(df.reset_index(drop=False), id_vars=['L0'], var_name='L1', value_name='L2').dropna()
    df = df.explode(column='L2')
    return df

def create_csv_from_yml():
    fn = 'categorytree.yml'
    fn_csv = '.'.join(fn.split('.')[:-1])+'.csv'
    projdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wdir = os.path.join(projdir, 'hierarchy')
    seeddir = os.path.join(projdir, 'comptesperso_dbt_sf', 'seeds')
    d = load_yaml(os.path.join(wdir, fn))
    df = load_dict_to_level_based_hierarchy(d)
    df.to_csv(os.path.join(seeddir, fn_csv), index=False)

if __name__ == '__main__':
    create_csv_from_yml()