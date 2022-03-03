class OrderTransactionNode:
    def __init__(self, order):
        self.order = order
        self.next = None

class OrderTransactions:
    def __init__(self):
        self.head = None
        # self.tail = None

    def push(self, order):
        order_node = OrderTransactionNode(order)
        # newest transacted order should be at the head
        # and oldest transacted order should be last

        if not self.head:
            self.head = order_node
            return
        else:
            temp = self.head
            while not temp.next is None:
                temp = temp.next
            temp.next = order_node
            order_node.prev = temp

    def __iter__(self):
        order_node = self.head
        while order_node is not None:
            yield order_node.order
            order_node = order_node.next

    def show_orders(self):
        tmp = []
        for order in self:
            tmp.append(order)
        return tmp

    def last_order(self, order):
        orders = self.show_orders()[::-1][1:]

        for i in orders:
            if i != order and i.ticker == order.ticker:
                return order
        return None
