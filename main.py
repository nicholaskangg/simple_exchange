from models.OrderBook import OrderBook
from models.Order import Order

if __name__ == '__main__':
    # this run the sample program as illustrated on the worksheet

    # init orderbook
    order_book = OrderBook()

    def to_money(amount):
        return "{:,.2f}".format(amount)

    def get_context_str(order):
        if order.type == 'LMT':
            return f"You have placed a limit buy order for {order.quantity} {order.ticker} shares at ${to_money(order.price)} each."
        elif order.type == 'MKT':
            return f"You have placed a market order for {order.quantity} {order.ticker} shares."

    def bid_list(ticker):
        return order_book.bids.order_map[ticker]

    def ask_list(ticker):
        return order_book.asks.order_map[ticker]

    def get_quote(bid_list, ask_list):
        if bid_list.head and ask_list.head:
            last_ask = order_book.transactions.last_order(ask_list.head)
            if last_ask:
                print(f'{ticker} BID: ${bid_list.head.price}  ASK: ${to_money(ask_list.head.price)} LAST: ${to_money(last_ask.price)}')
            else:
                print(
                    f'{ticker} BID: ${to_money(bid_list.head.price)}  ASK: ${to_money(ask_list.head.price)} LAST: None')

        if ask_list.head and not bid_list.head:
            last_ask = order_book.transactions.last_order(ask_list.head)
            if last_ask:
                print(
                    f'{ticker} BID: None  ASK: ${to_money(ask_list.head.price)} LAST: {to_money(last_ask.price)}')
            else:
                print(
                    f'{ticker} BID: None  ASK: ${to_money(ask_list.head.price)} LAST: None')

        if bid_list.head and not ask_list.head:
            print(f'{ticker} BID: ${to_money(bid_list.head.price)}  ASK: None  LAST: None')


    while True:
        # user_inputs examples (Note: do not add in the ($) dollar sign)

        # BUY SNAP LMT 30 100
        # BUY FB MKT 20
        # VIEW ORDERS
        # SELL FB LMT 20.00 20
        # VIEW ORDERS
        # SELL SNAP LMT 30.00 20
        # VIEW ORDERS
        # SELL SNAP LMT 31.00 10
        # QUOTE SNAP

        user_input = str(input(f"\nKey in an action:\n{'---'*10}\n")).upper()
        if user_input == 'QUIT':
            break

        user_input_split = user_input.split(' ')
        if user_input_split[0] in ('BUY', 'SELL'):
            order = Order(user_input)
            order_book.append_order(order)
            print(get_context_str(order))

        elif user_input == 'VIEW ORDERS':
            A = order_book.transactions.show_orders()
            for i in range(0, len(A)):
                print(f'{i+1}. {A[i].to_string()}')

        elif user_input_split[0] == 'QUOTE':
            ticker = user_input_split[1]
            bid_list = bid_list(ticker)
            ask_list = ask_list(ticker)
            get_quote(bid_list, ask_list)






