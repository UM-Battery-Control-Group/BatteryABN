import os
import pytest
from pathlib import Path
import pandas as pd


from batteryabn.utils import Utils

ENV_PATH = Path(__file__).parent.parent.parent / 'data' / '.env.example'

@pytest.mark.utils
def test_load_env():
    Utils.load_env(ENV_PATH)
    assert os.getenv('ENV') == 'dev'

@pytest.mark.utils
def test_utils_drop_empty_rows():
    test_df = pd.DataFrame({
        'A': [1.0, 2.0, None],
        'B': [None, None, None],
        'C': ['a', 'b', None],
    })
    assert len(test_df) == 3, 'Test DataFrame should have 3 rows'
    new_df = Utils.drop_empty_rows(test_df)
    assert len(new_df) == 2, 'New DataFrame should have 2 rows'
    assert new_df.equals(pd.DataFrame({
        'A': [1.0, 2.0],
        'B': [None, None],
        'C': ['a', 'b'],
    })), 'New DataFrame should equal expected DataFrame'