class OrderList:
    def __init__(self, _type):
        self.type = _type
        self.head = None
        self.tail = None

    def remove_head(self):
        if not self.head.next:
            self.head = None
            self.tail = self.head
            return
        self.head = self.head.next

    def insert_at_head(self, order):
        order.next = self.head
        self.head = order

    def insert(self, order):

        if self.type == 'BUY':
            # insert by descending order
            if not self.head:
                order.next = self.head
                self.head = order
            elif self.head.type == 'MKT':
                self.insert_market_order(order)

            elif self.head.price <= order.price:
                order.next = self.head
                self.head = order

            else:
                # Locate the node before the point of insertion
                current = self.head
                while (current.next is not None and
                       current.next.price > order.price):
                    current = current.next

                order.next = current.next
                current.next = order

        elif self.type == 'SELL':
            # insert by ascending order
            if not self.head:
                order.next = self.head
                self.head = order

            elif self.head.type == 'MKT':
                self.insert_market_order(order)


            elif self.head.price >= order.price:
                order.next = self.head
                self.head = order

            else:

                # Locate the node before the point of insertion
                current = self.head
                while (current.next is not None and
                       current.next.price < order.price):
                    current = current.next

                order.next = current.next
                current.next = order

    def insert_market_order(self, order):
        current = self.head
        while (current.next is not None and
               current.next.type == 'MKT'):
            current = current.next

        order.next = current.next
        current.next = order

    def print_orders(self):
        order = self.head
        orders = []
        while order:
            orders.append(order.to_string())
            order = order.next

        return orders



