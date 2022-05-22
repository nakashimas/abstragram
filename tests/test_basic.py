
import unittest

class TestBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_basic(self):
        print("")
        import abstragram
        print("____ ____ ____ ____ ____ ____ ____ ____")
        print("TEST:","test_basic")
        _abs = abstragram.Abstragram(["mondrian composition"])
        print("____ ____ ____ ____ ____ ____ ____ ____")
if __name__ == "__main__":
    pass
