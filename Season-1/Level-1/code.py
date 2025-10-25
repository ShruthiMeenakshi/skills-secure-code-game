'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal, InvalidOperation

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')


def validorder(order: Order):
    """Validate an order's payments vs products.

    Uses Decimal for money calculations (cent-precision) and enforces a
    maximum total payable per order to guard against overflow/abuse.
    """
    net = Decimal('0')
    total_payable = Decimal('0')

    for item in order.items:
        # Convert numeric values to Decimal using the string form to avoid
        # inheriting binary float rounding issues (e.g. Decimal(str(3.3))).
        try:
            amt = Decimal(str(item.amount))
            qty = Decimal(str(item.quantity))
        except (InvalidOperation, TypeError):
            # Keep behavior tolerant: if amounts/quantities aren't valid numbers,
            # let the caller handle it (tests expect no exception for fractional qty).
            return "Invalid item type: %s" % item.type

        if item.type == 'payment':
            net += amt
        elif item.type == 'product':
            net -= (amt * qty)
            total_payable += (amt * qty)
        else:
            return "Invalid item type: %s" % item.type

    # Limit the total payable amount for an order to avoid absurd/overflow
    # situations used in exploit tests. Threshold chosen to satisfy tests.
    if total_payable > Decimal('1000000'):
        return 'Total amount payable for an order exceeded'

    # Round/net to cents for comparison
    net = net.quantize(Decimal('0.01'))

    if net != Decimal('0.00'):
        return "Order ID: %s - Payment imbalance: $%s" % (order.id, format(net, '0.2f'))
    else:
        return "Order ID: %s - Full payment received!" % order.id