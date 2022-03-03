import unittest
import inspect
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'exchange_demo')))

from models.OrderBook import OrderBook
from models.Order import Order


class TestOrderList(unittest.TestCase):
    # def setUp(self):
    #     pass

    def testBids(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        self.order_book = OrderBook()
        order1 = Order('BUY SNAP LMT 2 100')
        order2 = Order('BUY SNAP LMT 4 120')
        order3 = Order('BUY SNAP LMT 6 115')
        order4 = Order('BUY SNAP MKT 111')
        order5 = Order('BUY SNAP LMT 8 113')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)
        self.order_book.append_order(order4)
        self.order_book.append_order(order5)

        # should be in price descending order
        # if order type is a market order, we follow LIFO
        expected = [
            'BUY SNAP MKT 0/111 PENDING',
            'BUY SNAP LMT 8.0 0/113 PENDING',
            'BUY SNAP LMT 6.0 0/115 PENDING',
            'BUY SNAP LMT 4.0 0/120 PENDING',
            'BUY SNAP LMT 2.0 0/100 PENDING'
        ]

        llist = self.order_book.bids.order_map['SNAP']
        self.assertEqual(llist.print_orders(), expected)


    def testAsks(self):
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        self.order_book = OrderBook()
        order1 = Order('SELL SNAP LMT 8 100')
        order2 = Order('SELL SNAP LMT 6 120')
        order3 = Order('SELL SNAP MKT 120')
        order4 = Order('SELL SNAP LMT 4 115')
        order5 = Order('SELL SNAP MKT 100')
        order6 = Order('SELL SNAP LMT 2 113')

        self.order_book.append_order(order1)
        self.order_book.append_order(order2)
        self.order_book.append_order(order3)
        self.order_book.append_order(order4)
        self.order_book.append_order(order5)
        self.order_book.append_order(order6)

        # should be in price ascending order
        # if order type is a market order, we follow LIFO
        expected = ['SELL SNAP MKT 0/100 PENDING',
                    'SELL SNAP MKT 0/120 PENDING',
                    'SELL SNAP LMT 2.0 0/113 PENDING',
                    'SELL SNAP LMT 4.0 0/115 PENDING',
                    'SELL SNAP LMT 6.0 0/120 PENDING',
                    'SELL SNAP LMT 8.0 0/100 PENDING']

        llist = self.order_book.asks.order_map['SNAP']
        self.assertEqual(llist.print_orders(), expected)

    def runTest(self):
        self.testBids()
        self.testAsks()

if __name__ == '__main__':
    unittest.main()