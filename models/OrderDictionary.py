from models.OrderList import OrderList

class OrderDictionary:
    def __init__(self):
        self.order_map = {}

    def create_list(self, order, _type):
        self.order_map[order.ticker] = OrderList(_type)
        return self.order_map[order.ticker]