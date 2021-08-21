from prelude import *

import lufinance as lf
from lufinance import utils as ut


# case = {
#     'contract_name': 'BABA230616P00350000',
#     'last_trade_date': '2021-06-22 19:21:00',
#     'strike': 350.0,
#     'last_price': 145.94,
#     'bid': 140.45,
#     'ask': 142.0,
#     'change': 0.0,
#     'percent_change': 0.0,
#     'volume': '2',
#     'open_interest': 9,
#     'implied_volatility': 0.0,
#     'option_type': 'CALL',
#     'captured_at': '2021-08-13 06:06:25.131000',
#     'bid_ask': 1.5500000000000114,
#     'ticker': 'BABA',
#     'expiration_date': '2023-06-16 00:00:00'
# }

# assert lf.Option(case).as_dict() == case

# exp_cycle = lf.ExpirationCycle.from_symbol_expiry_pair('AAPL')

import unittest

import random
import string


def ticker_generator(size=random.randint(1,4), chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_option_dict_test_case():
    strike = random.uniform(0, 3000)
    price = random.uniform(100, 5000)
    case = {
        'contract_name': ticker_generator(size=20, chars=string.ascii_uppercase + string.digits),
        'last_trade_date': ut.now(),
        'strike': strike,
        'last_price': price,
        'bid': price + random.uniform(-price * 0.01, price * 0.01),
        'ask': price + random.uniform(-price * 0.01, price * 0.01),
        'change': random.uniform(0,10),
        'percent_change': random.uniform(0,1),
        'volume': random.uniform(0, 1000000),
        'open_interest': random.uniform(0, 100),
        'implied_volatility': random.uniform(0, 1),
        'option_type': 'CALL' if random.uniform(0,1) > 0.5 else 'PUT',
        'captured_at': ut.now(),
        'bid_ask': 0,
        'ticker': ticker_generator(),
        'expiration_date': ut.day_delta(random.randint(1,365))
    }
    return case

option_dicts = [generate_option_dict_test_case() for _ in range(100)]

class TestOption(unittest.TestCase):

    properties = {
        'contract_name',
        'last_trade_date',
        'strike',
        'last_price',
        'bid',
        'ask',
        'change',
        'percent_change',
        'volume',
        'open_interest',
        'implied_volatility',
        'option_type',
        'captured_at',
        'bid_ask',
        'ticker',
        'expiration_date'
    }

    def test_properties(self):
        for opt_dict in option_dicts:
            option = lf.Option(opt_dict)
            self.assertEqual(option.as_dict(), opt_dict)

if __name__ == '__main__':
    unittest.main()
