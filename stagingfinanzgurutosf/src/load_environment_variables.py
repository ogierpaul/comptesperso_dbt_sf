import os
from configparser import ConfigParser

hello_secret_key = 'HELLO_ACTION_MOVIE'
hello_secret_value = 'My favorite action movies are Top Gun and Mad Max'
local_path = '/Users/paul_ogier/.environment_variables/comptesperso_dbt_sf/dev/.env'
local_config_section = 'LOCAL'
expected_env_variables = [
    hello_secret_key,
    'SF_ACCOUNT',
    'SF_DATABASE',
    'SF_SCHEMA',
    'SF_USER',
    'SF_PASSWORD',
    'SF_ROLE',
    'SF_WAREHOUSE'
]


def set_env_variables_if_missing():
    cfg = ConfigParser()
    if os.environ.get(hello_secret_key) is None:
        cfg.read(local_path)
        d = dict(cfg.items(local_config_section))
        for k in d.keys():
            os.environ[k.upper()] = d[k]
    else:
        pass
    return None


def verify_env_variables_exist():
    return all([os.environ.get(e) is not None for e in expected_env_variables])

if __name__ == '__main__':
    set_env_variables_if_missing()
    print(verify_env_variables_exist())
    print(list(filter(lambda e: os.environ.get(e) is None, expected_env_variables)))
