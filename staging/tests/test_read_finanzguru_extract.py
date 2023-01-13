from unittest import TestCase
import pandas as pd
from staging.src.read_finanzguru_extract import hello_world



class Test(TestCase):
    def test_hello_world(self):
        assert hello_world() == 'Hello World'

    def test_remove_unused_cols(self):
        assert True


