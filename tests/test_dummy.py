import time

def test_thing(simvue):
    time.sleep(10)
    assert True


def test_other_thing(simvue):
    time.sleep(5)
    assert False
