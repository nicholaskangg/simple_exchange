import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'exchange_demo')))
import inspect

from models.OrderBook import OrderBook
from models.Order import Order
import unittest


class TestMarketOrderMatching(unittest.TestCase):
    def bid_list(self, ticker):
        return self.order_book.bids.order_map[ticker]

    def ask_list(self, ticker):
        return self.order_book.asks.order_map[ticker]

    def testMarketOrderMatching1(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 1
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP LMT 8 30')
        order2 = Order('BUY SNAP LMT 5 30')
        order3 = Order('BUY SNAP MKT 50')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)

        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(order3.filled_price, 8.0)
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 8.0 30/30 FILLED'])
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP MKT 30/50 PARTIAL', 'BUY SNAP LMT 5.0 0/30 PENDING'])

    def testMarketOrderMatching2(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 2
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 8 30')
        order2 = Order('SELL SNAP LMT 10 30')
        order3 = Order('SELL SNAP MKT 50')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)


        self.assertEqual(order3.filled_price, 8.0)
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 8.0 30/30 FILLED'])
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP MKT 30/50 PARTIAL', 'SELL SNAP LMT 10.0 0/30 PENDING'])

    def testMarketOrderMatching3(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 3: equal units
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP MKT 50')
        order2 = Order('SELL SNAP LMT 10 50')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP MKT 50/50 FILLED', 'SELL SNAP LMT 10.0 50/50 FILLED'])

    def testMarketOrderMatching4(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 4: more sell order limit units to market orders
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP MKT 50')
        order2 = Order('SELL SNAP LMT 10 70')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 10.0 50/70 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP MKT 50/50 FILLED'])

    def testMarketOrderMatching5(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 5: lesser sell order limit units to market orders
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP MKT 50')
        order2 = Order('SELL SNAP LMT 10 20')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP MKT 20/50 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 20/20 FILLED'])

    def testMarketOrderMatching6(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 6: the head of sell order book has not enough units to fill, we move to the next limit order
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP LMT 10 20')
        order2 = Order('SELL SNAP LMT 11 30')
        order3 = Order('BUY SNAP MKT 45')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)


        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP LMT 11.0 25/30 PARTIAL'])
        self.assertEqual(order3.filled_price, 11.0) # last filled price
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP LMT 10.0 20/20 FILLED', 'BUY SNAP MKT 45/45 FILLED'])

    def runTest(self):
        self.testMarketOrderMatching1()
        self.testMarketOrderMatching2()
        self.testMarketOrderMatching3()
        self.testMarketOrderMatching4()
        self.testMarketOrderMatching5()
        self.testMarketOrderMatching6()


if __name__ == '__main__':
    unittest.main()