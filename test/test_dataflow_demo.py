from openalea.core.alea import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

pm = PackageManager()
pm.init(verbose=False)

app = QApplication([])

def test_demo_weberpenn():
    """ Test dataflow demo WeberPenn"""
    res = run(('demo.weberpenn', 'Demo_WeberPenn'), {}, pm=pm)
    assert res == []

def _test_demo_weberpenn_grp_1():
    """ Test dataflow demo WeberPenn grp 1"""
    res = run(('demo.weberpenn', 'Demo_WeberPenn_grp_1'), {}, pm=pm)
    print res

def test_demo_weberpenn_test_quakingaspen():
    """ Test dataflow demo WeberPenn test_quakingaspen"""
    res = run(('demo.weberpenn', 'test_quakingaspen'), {}, pm=pm)
    assert res == []


