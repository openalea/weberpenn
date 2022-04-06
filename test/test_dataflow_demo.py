run_test = True
try:
    from openalea.core.alea import *
except:
    run_test = False

if run_test:
    pm = PackageManager()
    pm.init(verbose=False)

    def test_demo_weberpenn():
        """ Test dataflow demo WeberPenn"""
        res = run(('demo.weberpenn', 'Demo_WeberPenn'), {}, pm=pm)
        assert res == []


    def _test_demo_weberpenn_grp_1():
        """ Test dataflow demo WeberPenn grp 1"""
        res = run(('demo.weberpenn', 'Demo_WeberPenn_grp_1'), {}, pm=pm)
        print(res)


    def test_demo_weberpenn_test_quakingaspen():
        """ Test dataflow demo WeberPenn test_quakingaspen"""
        res = run(('demo.weberpenn', 'test_quakingaspen'), {}, pm=pm)
        assert res == []
