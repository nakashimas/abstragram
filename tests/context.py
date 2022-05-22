import unittest
class Context(unittest.TestCase):
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
    def context(self):
        print("")
        print("____ ____ ____ ____ ____ ____ ____ ____")
        print("TEST:","context")
        print("____ ____ ____ ____ ____ ____ ____ ____")
if __name__ == "__main__":
    pass
