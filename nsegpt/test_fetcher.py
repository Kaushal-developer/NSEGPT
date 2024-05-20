import unittest
from nsegpt.fetcher import NSEFETCHER

class TestNSEFetcher(unittest.TestCase):

    def test_fetcher_initialization(self):
        fetcher = NSEFETCHER(["RELIANCE", "TCS"])
        self.assertEqual(fetcher.stock_codes, ["RELIANCE", "TCS"])

    def test_gather_all_data(self):
        fetcher = NSEFETCHER(["RELIANCE"])
        data = fetcher.gather_all_data()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertTrue("stock_code" in data[0])

if __name__ == '__main__':
    unittest.main()
