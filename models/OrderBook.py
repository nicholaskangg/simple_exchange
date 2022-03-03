from models.OrderTransactions import OrderTransactions
from models.OrderDictionary import OrderDictionary

class OrderBook:
    def __init__(self):
        self.asks = OrderDictionary()
        self.bids = OrderDictionary()
        self.transactions = OrderTransactions()
        self.filled_transactions = []

    def append_order(self, order):
        if order.type == 'LMT':
            self.transactions.push(order)
            self.process_limit_order(order)
        elif order.type == 'MKT':
            self.transactions.push(order)
            self.process_market_order(order)

    def get_order_list(self, order):
        try:
            bid_list = self.bids.order_map[order.ticker]
        except:
            bid_list = self.bids.create_list(order, 'BUY')
        try:
            ask_list = self.asks.order_map[order.ticker]
        except:
            ask_list = self.asks.create_list(order, 'SELL')

        return bid_list, ask_list

    def process_limit_order(self, order):
        bid_list, ask_list = self.get_order_list(order)

        if order.action == 'BUY':
            if ask_list.head:
                if ask_list.head.type == 'MKT':
                    is_market_order = True
                else:
                    is_market_order = False

                if ask_list.head.type == 'LMT':
                    ask_price_is_lower = ask_list.head.price <= order.price
                else:
                    ask_price_is_lower = False

            # if head of orderbook is not empty and there is a matching price we start finding a match
            if ask_list.head and (ask_price_is_lower or is_market_order):
                # perfect match
                if ask_list.head.quantity == order.quantity:

                    if is_market_order:
                        ask_list.head.filled_price = order.price

                    qty = order.quantity
                    ask_list.head.quantity -= qty
                    order.quantity -= qty

                    ask_list.head.filled_price = order.price
                    ask_list.head.state = 'FILLED'
                    order.state = 'FILLED'
                    # self.transactions.push(ask_list.head)
                    # self.transactions.push(order)
                    self.filled_transactions.append(ask_list.head.to_string())
                    self.filled_transactions.append(order.to_string())

                    ask_list.remove_head()
                # all bids can be matched
                else:
                    if ask_list.head.quantity < order.quantity:

                        # keep looping to match all bids
                        if ask_list.head.type == 'LMT':
                            while order.quantity != 0 and ask_list.head and ask_list.head.price <= order.price:
                                if ask_list.head.quantity == order.quantity:
                                    # all bids are finally matched
                                    qty = order.quantity
                                    ask_list.head.quantity -= qty
                                    order.quantity -= qty
                                    # self.transactions.push(ask_list.head)
                                    self.filled_transactions.append(ask_list.head.to_string())
                                    ask_list.remove_head()
                                elif ask_list.head.quantity < order.quantity:
                                    # not enough orders at the head, remove head to get to the new head
                                    qty = ask_list.head.quantity
                                    order.quantity -= qty
                                    ask_list.head.quantity -= qty
                                    ask_list.head.state = 'FILLED'
                                    # self.transactions.push(ask_list.head)
                                    self.filled_transactions.append(ask_list.head.to_string())
                                    ask_list.remove_head()

                                else:
                                    ask_list.head.state = order.state = 'PARTIAL'
                                    qty = order.quantity
                                    order.quantity -= qty
                                    ask_list.head.quantity -= qty

                            if order.quantity != 0:
                                # remaining quantity cannot be match, so we create an order in bids
                                order.state = "PARTIAL"

                                bid_list.insert(order)

                        elif ask_list.head.type == 'MKT':
                            while order.quantity != 0 and ask_list.head:
                                if ask_list.head.quantity == order.quantity:
                                    # all bids are finally matched
                                    qty = order.quantity
                                    ask_list.head.quantity -= qty
                                    order.quantity -= qty
                                    # self.transactions.push(ask_list.head)
                                    self.filled_transactions.append(ask_list.head.to_string())
                                    ask_list.remove_head()
                                elif ask_list.head.quantity < order.quantity:
                                    # not enough orders at the head, remove head to get to the new head

                                    order.quantity -= ask_list.head.quantity
                                    ask_list.head.quantity = 0
                                    ask_list.head.state = 'FILLED'
                                    # self.transactions.push(ask_list.head)
                                    self.filled_transactions.append(ask_list.head.to_string())
                                    ask_list.head.filled_price = order.price

                                    ask_list.remove_head()
                                else:
                                    ask_list.head.state = order.state = 'PARTIAL'
                                    qty = order.quantity
                                    order.quantity -= qty
                                    ask_list.head.quantity -= qty

                            if order.quantity != 0:
                                # remaining quantity cannot be match, so we create an order in bids
                                order.state = "PARTIAL"
                                bid_list.insert(order)

                    elif ask_list.head.quantity > order.quantity:
                        if order.quantity != 0 and ask_list.head and (is_market_order or ask_price_is_lower):
                            if is_market_order:
                                ask_list.head.filled_price = order.price

                            qty = order.quantity
                            order.quantity -= qty
                            ask_list.head.quantity -= qty
                            ask_list.head.state = 'PARTIAL'
                            order.state = "FILLED"
                            # self.transactions.push(order)
                            self.filled_transactions.append(order.to_string())

            else:
                # append to bids orderbook if asks is empty
                bid_list.insert(order)

        elif order.action == 'SELL':

            if bid_list.head and bid_list.head.type == 'LMT':

                if bid_list.head.price >= order.price:
                    if bid_list.head.quantity == order.quantity:
                        qty = order.quantity
                        bid_list.head.quantity -= qty
                        order.quantity -= qty

                        bid_list.head.filled_price = order.price
                        bid_list.head.state = 'FILLED'
                        order.state = 'FILLED'
                        # self.transactions.push(bid_list.head)
                        # self.transactions.push(order)
                        self.filled_transactions.append(bid_list.to_string())
                        self.filled_transactions.append(order.to_string())
                        bid_list.remove_head()
                    else:
                        if bid_list.head.quantity < order.quantity:
                            while order.quantity != 0 and bid_list.head and bid_list.head.price >= order.price:
                                if bid_list.head.quantity == order.quantity:
                                    # all asks are finally matched
                                    ask_list.head.state = 'FILLED'
                                    self.filled_transactions.append(ask_list.head.to_string())
                                    # self.transactions.push(ask_list.head)
                                    ask_list.remove_head()
                                elif bid_list.head.quantity < order.quantity:
                                    # not enough orders at the head, remove head to get to the new head
                                    order.state = 'PARTIAL'
                                    order.quantity -= bid_list.head.quantity
                                    bid_list.head.quantity = 0
                                    bid_list.head.state = 'FILLED'
                                    # self.transactions.push(bid_list.head)
                                    self.filled_transactions.append(bid_list.head.to_string())
                                    bid_list.remove_head()
                                else:
                                    bid_list.head.state = order.state = 'PARTIAL'
                                    qty = order.quantity
                                    order.quantity -= qty
                                    bid_list.head.quantity -= qty

                            if order.quantity != 0:
                                # remaining quantity cannot be match, so we create an order in asks
                                order.state = "PARTIAL"
                                ask_list.insert(order)

                        elif bid_list.head.quantity > order.quantity:
                            if order.quantity != 0 and bid_list.head and bid_list.head.price <= order.price:

                                qty = order.quantity
                                order.quantity -= qty
                                bid_list.head.quantity -= qty
                                bid_list.head.state = 'PARTIAL'
                                order.state = "FILLED"
                                # self.transactions.push(order)
                                self.filled_transactions.append(order.to_string())
                else:
                    # append to bids orderbook if asks is empty
                    ask_list.insert(order)

            elif bid_list.head and bid_list.head.type == 'MKT':
                if bid_list.head.quantity == order.quantity:
                    qty = order.quantity
                    bid_list.head.quantity -= qty
                    order.quantity -= qty

                    bid_list.head.filled_price = order.price
                    bid_list.head.state = 'FILLED'
                    order.state = 'FILLED'
                    # self.transactions.push(bid_list.head)
                    # self.transactions.push(order)
                    self.filled_transactions.append(bid_list.head.to_string())
                    self.filled_transactions.append(order.to_string())
                    bid_list.remove_head()
                else:
                    if bid_list.head.quantity < order.quantity:
                        while order.quantity != 0 and bid_list.head:
                            if bid_list.head.quantity == order.quantity:
                                # all asks are finally matched
                                ask_list.head.state = 'FILLED'
                                self.filled_transactions.append(ask_list.head.to_string())
                                # self.transactions.push(ask_list.head)
                                ask_list.remove_head()
                            elif bid_list.head.quantity < order.quantity:
                                # not enough orders at the head, remove head to get to the new head
                                order.state = 'PARTIAL'
                                order.quantity -= bid_list.head.quantity
                                bid_list.head.filled_price = order.price
                                bid_list.head.quantity = 0
                                bid_list.head.state = 'FILLED'
                                # self.transactions.push(bid_list.head)
                                self.filled_transactions.append(bid_list.head.to_string())
                                bid_list.remove_head()
                            else:
                                bid_list.head.state = order.state = 'PARTIAL'
                                qty = order.quantity
                                order.quantity -= qty
                                bid_list.head.quantity -= qty

                        if order.quantity != 0:
                            # remaining quantity cannot be match, so we create an order in asks
                            order.state = "PARTIAL"
                            ask_list.insert(order)

                    elif bid_list.head.quantity > order.quantity:
                        if order.quantity != 0 and bid_list.head:

                            qty = order.quantity
                            order.quantity -= qty
                            bid_list.head.quantity -= qty
                            bid_list.head.state = 'PARTIAL'
                            bid_list.head.filled_price = order.price
                            order.state = "FILLED"
                            # self.transactions.push(order)
                            self.filled_transactions.append(order.to_string())
            else:
                # append to bids orderbook if asks is empty
                if order.type == 'MKT':
                    ask_list.insert_at_head(order)
                else:
                    ask_list.insert(order)

    def process_market_order(self, order):
        bid_list, ask_list = self.get_order_list(order)

        if order.action == 'BUY':
            # if head of order book is not empty and there is a sell limit order, we match.
            if ask_list.head:
                if ask_list.head.quantity == order.quantity:
                    # ask_list.state()
                    ask_list.remove_head()

                # all bids can be matched
                else:
                    if ask_list.head.quantity < order.quantity:

                        # keep looping to match all bids
                        while order.quantity != 0 and ask_list.head:
                            if ask_list.head.quantity == order.quantity:
                                # all bids are finally matched
                                qty = order.quantity
                                ask_list.head.quantity -= qty
                                order.quantity -= qty
                                # self.transactions.push(ask_list.head)
                                self.filled_transactions.append(ask_list.head.to_string())

                                ask_list.remove_head()
                            elif ask_list.head.quantity < order.quantity:
                                # not enough orders at the head, remove head to get to the new head
                                order.quantity -= ask_list.head.quantity
                                ask_list.head.quantity = 0
                                ask_list.head.state = 'FILLED'
                                order.filled_price = ask_list.head.price
                                # self.transactions.push(ask_list.head)
                                self.filled_transactions.append(ask_list.head.to_string())
                                ask_list.remove_head()
                            else:
                                ask_list.head.state = 'PARTIAL'
                                qty = order.quantity
                                order.quantity -= qty
                                ask_list.head.quantity -= qty
                                order.filled_price = ask_list.head.price
                                if order.quantity == 0:
                                    order.state = 'FILLED'
                                    # self.transactions.push(order)
                                    self.filled_transactions.append(order.to_string())
                                else:
                                    order.state = 'PARTIAL'

                        if order.quantity != 0:
                            # remaining quantity cannot be match, so we create an order in bids
                            order.state = "PARTIAL"
                            bid_list.insert_at_head(order)

                    elif ask_list.head.quantity > order.quantity:
                        if order.quantity != 0 and ask_list.head:
                            qty = order.quantity
                            order.quantity -= qty
                            ask_list.head.quantity -= qty
                            ask_list.head.state = 'PARTIAL'

                            order.state = "FILLED"
                            # self.transactions.push(order)
                            self.filled_transactions.append(order.to_string())

            else:
                # append to bids orderbook if asks is empty
                bid_list.insert_at_head(order)

        elif order.action == 'SELL':
            if bid_list.head:
                if bid_list.head.quantity == order.quantity:
                    bid_list.head.remove_head()
                else:
                    if bid_list.head.quantity < order.quantity:
                        while order.quantity != 0 and bid_list.head:
                            if bid_list.head.quantity == order.quantity:
                                # all asks are finally matched
                                ask_list.head.state = 'FILLED'
                                # self.transactions.push(ask_list.head)
                                self.filled_transactions.append(ask_list.head.to_string())
                                ask_list.remove_head()
                            elif bid_list.head.quantity < order.quantity:
                                # not enough orders at the head, remove head to get to the new head
                                order.state = 'PARTIAL'
                                order.quantity -= bid_list.head.quantity
                                order.filled_price = bid_list.head.price
                                bid_list.head.quantity = 0
                                bid_list.head.state = 'FILLED'
                                # self.transactions.push(bid_list.head)
                                self.filled_transactions.append(bid_list.head.to_string())
                                bid_list.remove_head()
                            else:
                                bid_list.head.state = order.state = 'PARTIAL'
                                qty = order.quantity
                                order.quantity -= qty
                                bid_list.head.quantity -= qty

                                if order.quantity == 0:
                                    order.state = 'FILLED'
                                    # self.transactions.push(order)
                                    self.filled_transactions.append(order.to_string())

                        if order.quantity != 0:
                            # remaining quantity cannot be match, so we create an order in asks
                            order.state = "PARTIAL"
                            ask_list.insert_at_head(order)

                    elif bid_list.head.quantity > order.quantity:
                        if order.quantity != 0 and bid_list.head:

                            qty = order.quantity
                            order.quantity -= qty
                            bid_list.head.quantity -= qty
                            bid_list.head.state = 'PARTIAL'
                            order.state = "FILLED"
                            # self.transactions.push(order)
                            self.filled_transactions.append(order.to_string())

            else:
                # append to bids orderbook if asks is empty
                ask_list.insert_at_head(order)
