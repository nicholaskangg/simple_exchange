import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'exchange_demo')))
import inspect
from models.OrderBook import OrderBook
from models.Order import Order
import unittest


class TestMarketOrderMatching2(unittest.TestCase):
    """ This file TestMarketOrderMatching2 is similar to TestMarketOrderMatching but the order in which orders arrive is switched"""
    def bid_list(self, ticker):
        return self.order_book.bids.order_map[ticker]

    def ask_list(self, ticker):
        return self.order_book.asks.order_map[ticker]

    def testMarketOrderMatching1(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 1: equal units
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP MKT 50')
        order2 = Order('BUY SNAP LMT 10 50')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP MKT 50/50 FILLED', 'BUY SNAP LMT 10.0 50/50 FILLED'])

    def testMarketOrderMatching2(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 2: There are more BUY limit orders than SELL market orders
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP MKT 50')
        order2 = Order('BUY SNAP LMT 10 70')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 50/70 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(self.order_book.filled_transactions, ['SELL SNAP MKT 50/50 FILLED'])

    def testMarketOrderMatching3(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 3: There are lesser BUY limit orders than SELL market orders
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP MKT 50')
        order2 = Order('BUY SNAP LMT 10 20')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.assertEqual(order1.filled_price, 10.0)
        self.assertEqual(self.bid_list('SNAP').print_orders(), [])
        self.assertEqual(self.ask_list('SNAP').print_orders(), ['SELL SNAP MKT 20/50 PARTIAL'])
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 10.0 20/20 FILLED'])

    def testMarketOrderMatching4(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        # context 4: the head of the bid order book @ $10 does not enough units to fill, we move to the next limit order @ $11
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 10 20')
        order2 = Order('BUY SNAP LMT 11 30')
        order3 = Order('SELL SNAP MKT 45')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)


        self.assertEqual(self.bid_list('SNAP').print_orders(), ['BUY SNAP LMT 10.0 15/20 PARTIAL'])
        self.assertEqual(self.ask_list('SNAP').print_orders(), [])
        self.assertEqual(order3.filled_price, 11.0) # last filled price
        self.assertEqual(self.order_book.filled_transactions, ['BUY SNAP LMT 11.0 30/30 FILLED', 'SELL SNAP MKT 45/45 FILLED'])

    def runTest(self):
        self.testMarketOrderMatching1()
        self.testMarketOrderMatching2()
        self.testMarketOrderMatching3()
        self.testMarketOrderMatching4()


if __name__ == '__main__':
    unittest.main()



EURJPY
CADJPY
NZDJPY
EURCHF
NZDCHF
AUDCHF
AUDJPY
GBPCHF