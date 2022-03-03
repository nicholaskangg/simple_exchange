class Order:
    def __init__(self, data):
        self.data = data
        split_data = data.split(' ')
        self.type = split_data[2]

        if self.type == 'MKT':
            self.action = split_data[0]
            self.ticker = split_data[1]
            self.filled_price = 0
            self.quantity = int(split_data[3])
            self.amount_to_fill = int(split_data[3])

        elif self.type == 'LMT':
            self.action = split_data[0]
            self.ticker = split_data[1]
            self.price = float(split_data[3])
            self.quantity = int(split_data[4])
            self.amount_to_fill = int(split_data[4])

        else:
            raise ValueError('Invalid order type')

        # states: 'PENDING', 'PARTIAL', 'FILLED'
        self.state = 'PENDING'
        self.next = None
        self.prev = None

    def to_string(self):
        if self.type == 'LMT': return f'{self.action} {self.ticker} {self.type} {self.price} {self.amount_to_fill - self.quantity}/{self.amount_to_fill} {self.state}'
        if self.type == 'MKT': return f'{self.action} {self.ticker} {self.type} {self.amount_to_fill - self.quantity}/{self.amount_to_fill} {self.state}'
