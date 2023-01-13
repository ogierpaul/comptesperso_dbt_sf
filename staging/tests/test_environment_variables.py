import pytest
import os
import configparser
from staging.src import expected_env_variables, verify_env_variables_exist, set_env_variables_if_missing


def test_variables_exist():
    set_env_variables_if_missing()
    assert verify_env_variables_exist()