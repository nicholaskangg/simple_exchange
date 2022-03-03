from test.TestOrderTransactions import TestOrderTransactions
from test.TestLimitOrderMatching import TestLimitOrderMatching
from test.TestMarketOrderMatching import TestMarketOrderMatching
from test.TestMarketOrderMatching2 import TestMarketOrderMatching2
from test.TestOrderList import TestOrderList

import unittest

def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestOrderTransactions())
    test_suite.addTest(TestLimitOrderMatching())
    test_suite.addTest(TestMarketOrderMatching())
    test_suite.addTest(TestMarketOrderMatching2())
    test_suite.addTest(TestOrderList())

    return test_suite

if __name__ == '__main__':
   suite = create_suite()
   runner=unittest.TextTestRunner()
   runner.run(suite)