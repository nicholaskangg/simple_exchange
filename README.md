# Simple Stock Exchange
```python version 3.9```

### How to use?
1. The scenario for the worksheet where the user can input data can be run via ```main.py```
2. The full suite for the test cases can be run via ```run_all_test.py```

### How the exchange is implemented

The use of standard data structures allows easier implementation and performance.
Using OOP, the responsibilities are segregated in their classes which are stored in ```models``` folder.

1. ```Order``` class creates a new order.
2. When a order is created in can be added into the order book via ```OrderBook().append_order()```.
3. Depending on the order type (LMT/MKT), the order will then be processed where order matching will be done on the bid and ask ```OrderList```.
4. ```OrderDictionary``` is use to differentiate the respective ```OrderList``` according to their ticker
5. All orders are stored in ```OrderTransactions``` so that it can be easily retrieved.

### What can be done better?
1. The stock exchange exercise is implemented using a test driven development approach.
2. The code is lean and the test cases has been constructed to cover most edge cases, allowing for further refactoring.
3. Other features such as volume, market order functions such as FOK can be implemented.

# Thank you for you time! 


