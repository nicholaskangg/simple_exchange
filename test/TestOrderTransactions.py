import unittest
import inspect
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'exchange_demo')))

# Now do your import
from models.Order import Order
from models.OrderTransactions import OrderTransactions

class TestOrderTransactions(unittest.TestCase):
    def testPush(self):
        # context 1: the latest transaction should be at the head
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        order_transactions = OrderTransactions()
        order1 = Order('SELL SNAP LMT 8 30')
        order2 = Order('BUY SNAP LMT 5 30')
        order3 = Order('BUY SNAP MKT 30')

        order_transactions.push(order1)
        order_transactions.push(order2)
        order_transactions.push(order3)

        # breakpoint()
        self.assertEqual(order_transactions.head.order, order1)
        self.assertEqual(order_transactions.head.next.order, order2)
        self.assertEqual(order_transactions.head.next.next.order, order3)

    def testShowOrders(self):
        # context 2: the method should return a list of orders that has been transacted
        print(f'Testing... {__name__} -> method: {inspect.stack()[0][3]}')
        order_transactions = OrderTransactions()
        order1 = Order('SELL SNAP LMT 8 30')
        order2 = Order('BUY SNAP LMT 5 30')
        order3 = Order('BUY SNAP MKT 2 30')

        order_transactions.push(order1)
        order_transactions.push(order2)
        order_transactions.push(order3)

        arr = order_transactions.show_orders()

        self.assertEqual(arr[0], order1)
        self.assertEqual(arr[1], order2)
        self.assertEqual(arr[2], order3)

    def runTest(self):
        self.testPush()
        self.testShowOrders()


if __name__ == '__main__':
    unittest.main()