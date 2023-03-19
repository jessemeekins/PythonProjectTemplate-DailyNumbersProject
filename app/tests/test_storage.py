#%%

import pytest

try:
    import mylib
except ImportError:
    mylib = None

@pytest.mark.skip("Do not run this")
def test_true():
    assert True

def test_key():
    a = ['a', 'b']
    b = ['b']
    assert a != b

@pytest.mark.skipif(mylib is None, reason="mylib is unavailable")
def test_mylib():
    assert mylib.foobar() == 42


def test_skip_at_runtime():
    if True:
        pytest.skip("Finally, I dont want to run it.")