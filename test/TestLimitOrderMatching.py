import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'exchange_demo')))
import inspect

from models.OrderBook import OrderBook
from models.Order import Order
import unittest


class TestLimitOrderMatching(unittest.TestCase):
    def bid_list(self, ticker):
        return self.order_book.bids.order_map[ticker]

    def ask_list(self, ticker):
        return self.order_book.asks.order_map[ticker]

    def testLimitOrderMatching1(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # simple scenario 1
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP LMT 9.99 100') # -100 @ 9.99
        order2 = Order('BUY SNAP LMT 10 50') # -50 @ 9.99
        order3 = Order('BUY SNAP LMT 10 12') # -38 @ 9.99
        order4 = Order('BUY SNAP LMT 9.99 100') # +62 @ 9.99

        self.order_book.append_order(order1)
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 9.99 0/100 PENDING'])
        self.assertEqual(self.order_book.filled_transactions, [])
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])

        self.order_book.append_order(order2)
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 9.99 50/100 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 50/50 FILLED'])
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])

        self.order_book.append_order(order3)
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 9.99 62/100 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 50/50 FILLED', 'BUY SNAP LMT 10.0 12/12 FILLED'])
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])

        self.order_book.append_order(order4)
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 50/50 FILLED', 'BUY SNAP LMT 10.0 12/12 FILLED', 'SELL SNAP LMT 9.99 100/100 FILLED'])
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 9.99 38/100 PARTIAL'])


    def testLimitOrderMatching2(self):
        # simple scenario 2
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 10 100')
        order2 = Order('SELL SNAP LMT 10 50')
        order3 = Order('SELL SNAP LMT 10 12')
        order4 = Order('SELL SNAP LMT 12.50 50')

        self.order_book.append_order(order1)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 0/100 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, [])


        self.order_book.append_order(order2)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 50/100 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 50/50 FILLED'])

        self.order_book.append_order(order3)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 62/100 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 50/50 FILLED', 'SELL SNAP LMT 10.0 12/12 FILLED'])

        self.order_book.append_order(order4)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 62/100 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 12.5 0/50 PENDING'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 50/50 FILLED', 'SELL SNAP LMT 10.0 12/12 FILLED'])

    def testLimitOrderMatching3(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # simple scenario 3
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 10 100') # +100 @ $10
        order2 = Order('SELL SNAP LMT 10 150') # -50 @ $10
        order3 = Order('SELL SNAP LMT 8 30') # -30 @ $8, -50 @ $10
        order4 = Order('BUY SNAP LMT 10 50') # -30 @ $10

        self.order_book.append_order(order1)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 0/100 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])

        self.order_book.append_order(order2)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 100/150 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 100/100 FILLED'])

        self.order_book.append_order(order3)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(),
                         ['SELL SNAP LMT 8.0 0/30 PENDING', 'SELL SNAP LMT 10.0 100/150 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 100/100 FILLED'])
        #
        self.order_book.append_order(order4)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 120/150 PARTIAL'])

    def testLimitOrderMatching4(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # scenario 4: limit buy and sell with varying quantities and prices
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP LMT 8 30') # -30 @ $8
        order2 = Order('SELL SNAP LMT 10 50') # -30 @ $8, -50 @ $10
        order3 = Order('BUY SNAP LMT 10 50')  # -30 @ $10
        order4 = Order('BUY SNAP LMT 8 50')  # -30 @ $10, +50 @ $8
        order5 = Order('BUY SNAP LMT 11 20')  # -10 @ $10, +50 @ $8

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 20/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 8.0 30/30 FILLED'])

        self.order_book.append_order(order4)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/50 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 20/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 8.0 30/30 FILLED'])

        self.order_book.append_order(order5)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/50 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 8.0 30/30 FILLED', 'BUY SNAP LMT 11.0 20/20 FILLED'])

    def testLimitOrderMatching5(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # scenario 5: limit buy and sell of different stocks (SNAP and FB) with varying quantities and prices
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 8 30') # +30 @ $8
        order2 = Order('BUY SNAP LMT 10 50') # +50 @ $10, +30 @ $8
        order3 = Order('SELL SNAP LMT 10 10')  # [+40 @ $10, +30 @ $8]
        order4 = Order('SELL SNAP LMT 10 50')  # [+30 @ $8] and [-10 @ $10]

        order5 = Order('BUY FB LMT 8 30')
        order6 = Order('BUY FB LMT 10 50')
        order7 = Order('SELL FB LMT 10 10')
        order8 = Order('SELL FB LMT 10 50')

        self.order_book.append_order(order1)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, [])

        self.order_book.append_order(order2)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 0/50 PENDING', 'BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, [])

        self.order_book.append_order(order3)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 10/50 PARTIAL', 'BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 10/10 FILLED'])

        self.order_book.append_order(order4)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 10/10 FILLED', 'BUY SNAP LMT 10.0 50/50 FILLED'])

        self.order_book.append_order(order5)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.bid_list('FB').print_orders(), ['BUY FB LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('FB').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 10/10 FILLED', 'BUY SNAP LMT 10.0 50/50 FILLED'])

        self.order_book.append_order(order6)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.bid_list('FB').print_orders(), ['BUY FB LMT 10.0 0/50 PENDING', 'BUY FB LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('FB').print_orders(), [])

        self.order_book.append_order(order7)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.bid_list('FB').print_orders(), ['BUY FB LMT 10.0 10/50 PARTIAL', 'BUY FB LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('FB').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 10/10 FILLED',
                                                               'BUY SNAP LMT 10.0 50/50 FILLED',
                                                               'SELL FB LMT 10.0 10/10 FILLED'])

        self.order_book.append_order(order8)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.bid_list('FB').print_orders(), ['BUY FB LMT 8.0 0/30 PENDING'])
        self.assertEqual(self.ask_list('FB').print_orders(), ['SELL FB LMT 10.0 40/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 10/10 FILLED',
                                                               'BUY SNAP LMT 10.0 50/50 FILLED',
                                                               'SELL FB LMT 10.0 10/10 FILLED',
                                                               'BUY FB LMT 10.0 50/50 FILLED'])


    def runTest(self):
        self.testLimitOrderMatching1()
        self.testLimitOrderMatching2()
        self.testLimitOrderMatching3()
        self.testLimitOrderMatching4()
        self.testLimitOrderMatching5()

if __name__ == '__main__':
    unittest.main()