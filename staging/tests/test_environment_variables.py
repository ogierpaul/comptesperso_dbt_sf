import pytest
import os
import configparser
from staging.src import expected_env_variables, verify_env_variables_exist, set_env_variables_if_missing
from staging.src.load_environment_variables import hello_secret_key, hello_secret_value

def test_environment_variables_properly_set():
    set_env_variables_if_missing()
    assert verify_env_variables_exist()
    assert os.environ.get(hello_secret_key) == hello_secret_value
