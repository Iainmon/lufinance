# __all__ = ['option_chains', 'record_option_chains', 'scrape_tickers', 'Option', 'ExpirationCycle', 'Share']

##
## Lufrano Finance Library
## Copyright Iain Moncrief (Aug 12, 2021) - All rights reserved.
##

from typing import TypeVar, Generic

import yfinance as yf
# from yahoo_fin import options
import yahoo_fin as yfin
import pandas as pd
import json
from pandas.core.common import flatten
import numpy as np
import re
from datetime import datetime
import pytz
import cachetools.func


from qfin.options import BlackScholesCall
from qfin.options import BlackScholesPut


from . import live_data as live
from . import utils as ut


def preprocess_option_spread(record):
    new_record = {}
    for k, v in record.items():
        new_k = ut.camel_to_snake(k)
        tv = type(v)
        if tv is np.int64:
            new_record[new_k] = int(v)
        elif tv is np.bool_:
            new_record[new_k] = bool(v)
        else:
            new_record[new_k] = v
    return new_record

def parse_option_spreads(option_spreads):
    records = pd.DataFrame(option_spreads).to_dict('records')
    return [preprocess_option_spread(record) for record in records]


def record_option_chain(option_chain, ticker_symbol, expiration_date=None):
#     expiration_date = options.get_expiration_dates(ticker_symbol)[0] if expiration_date == None else expiration_date
    assert(not expiration_date is None)
#     calls = process_option_spreads(option_chain.calls)
    calls = parse_option_spreads(option_chain['calls'])
    for call in calls:
        call['option_type'] = 'CALL'
    
#     puts = process_option_spreads(option_chain.puts)
    puts = parse_option_spreads(option_chain['puts'])
    for put in puts:
        put['option_type'] = 'PUT'
    
    now = pd.Timestamp(datetime.now())
    processed_chain = calls + puts
    for processed in processed_chain:
        processed['captured_at'] = now
        
        dates = processed['last_trade_date'].split(' ', 2)
        date = f'{dates[0]} 0{dates[1]}'
        processed['last_trade_date'] = pd.Timestamp(date,tzinfo=pytz.timezone('US/Eastern'))
        processed['implied_volatility'] = np.float64(processed['implied_volatility'].replace('%',''))
        processed['percent_change'] = np.float64(0) if processed['percent_change'] == '-' else np.float64(processed['percent_change'].replace('%','').replace(',',''))
        
        processed['volume'] = np.float64(processed['volume'])
        processed['ask'] = np.float64(str(processed['ask']).replace(',',''))
        processed['bid'] = np.float64(str(processed['bid']).replace(',',''))
        processed['bid_ask'] = processed['ask'] - processed['bid']
        processed['ticker'] = ticker_symbol
        processed['expiration_date'] = pd.Timestamp(expiration_date)
        
    return processed_chain

def record_option_chains(tickers, dates=[],verbose=False):
    no_dates = len(dates) == 0
    chains = []
    for ticker in tickers:
        if no_dates:
            exp_dates = list(live.get_expiration_dates(ticker))
            dates = [str(pd.Timestamp(d).date()) for d in exp_dates]
        for date in dates:
            try:
                opts = live.get_options_chain(ticker,date=date)
                processed_chain = record_option_chain(opts, ticker, expiration_date=date)
                chains += processed_chain
            except ValueError as e:
                if verbose:
                    print(e)
                    print(f'Error: could not find option chain for {ticker} at expiration date {date}! Bumbai.')
                continue
    return chains

def scrape_tickers(tickers, dates=[], verbose=False):
    current_states = record_option_chains(tickers,dates,verbose=verbose)
    json_states = json.dumps(current_states)
    return json_states

def option_chains(*args):
    chains = record_option_chains(*args)
    return list(map(Option,chains))



class Asset():
    @property
    def asset_name(self):
        return self.__asset_name
    
    def __init__(self,asset_name):
        assert asset_name
        self.__asset_name = asset_name

class Share(Asset):

    aliases = {
        'premium': 'price',
        'stock_price': 'price'
    }
    
    def __setattr__(self, name, value):
        name = self.aliases.get(name, name)
        object.__setattr__(self, name, value)
    def __getattr__(self, name):
        if name == 'aliases':
            raise AttributeError
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)
    
    def __init__(self,dic):
        assert type(dic) is dict
        super().__init__(asset_name='share')
        

class Option(Asset):
    
    aliases = {
        'strike_price': 'strike',
        'iv': 'implied_volatility',
        'type': 'option_type',
        'symbol': 'contract_symbol',
    }

    stateful_methods = [
        'in_the_money',
        'current_asset_price'
    ]
    
    def __setattr__(self, name, value):
        name = self.aliases.get(name, name)
        object.__setattr__(self, name, value)
    def __getattr__(self, name):
        if name == 'aliases':
            raise AttributeError
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)
    
    def __init__(self, dic: dict[str, object]) -> None:
        assert type(dic) is dict
        super().__init__(asset_name='option')
        self.ticker = dic['ticker']
        self.contract_symbol = dic['contract_name'] if 'contract_name' in dic.keys() else dic['contract_symbol']
        self.option_type = str(dic['option_type'])
        self.strike = dic['strike']
        self.expiration_date = dic['expiration_date']
        self.last_price = dic['last_price']
        self.last_trade_date = dic['last_trade_date']
        self.bid = dic['bid']
        self.ask = dic['ask']
        self.bid_ask = dic['bid_ask']
        self.change = dic['change']
        self.percent_change = 0 if dic['percent_change'] is None else dic['percent_change']
        self.volume = dic['volume']
        self.open_interest = dic['open_interest']
        self.implied_volatility = dic['implied_volatility']
        self.captured_at = dic['captured_at']
        self.database_identifier = dic['_id'] if '_id' in dic.keys() else None
        
    def as_dict(self) -> dict[str, object]:
        return {
            **({ '_id' : self.database_identifier }
               if not self.database_identifier is None else {}),
            'contract_name': self.contract_symbol,
            'last_trade_date': self.last_trade_date,
            'strike': self.strike,
            'last_price': self.last_price,
            'bid': self.bid,
            'ask': self.ask,
            'change': self.change,
            'percent_change': self.percent_change,
            'volume': self.volume,
            'open_interest': self.open_interest,
            'implied_volatility': self.implied_volatility,
            'option_type': self.option_type,
            'captured_at': self.captured_at,
            'bid_ask': self.bid_ask,
            'ticker': self.ticker,
            'expiration_date': self.expiration_date
        }
    
    def as_json(self) -> str:
        dic = self.as_dict()
        json_str = json.dumps(dic,default=str)
        return json_str
    
    def current_asset_price(self) -> np.float64:
        current_price,_ = live.get_current_stock_price(self.ticker)
        return np.float64(current_price)
    
    def in_the_money(self) -> bool:
        current_price = self.current_asset_price()
        if self.option_type == 'CALL':
            return current_price > self.strike_price
        elif self.option_type == 'PUT':
            return current_price < self.strike_price
        
        raise ValueError(f'Option.option_type cannot be {self.option_type}')
        
    @staticmethod
    def collection_from_query(query: object) -> list[object]:
        return list(map(Option, list(query)))
    
    
    
class ExpirationCycle:
    
    aliases = {
        'options': 'chain',
        'contracts': 'chain'
    }
    
    def __setattr__(self, name, value):
        name = self.aliases.get(name, name)
        object.__setattr__(self, name, value)
    def __getattr__(self, name):
        if name == 'aliases':
            raise AttributeError
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)
    
    @property
    def chain(self) -> list[Option]:
        return self.__chain
    
    @property
    def cycle_type(self) -> str:
        if len(self.chain) < 1:
            return 'Call/Put'
        first_option = self.chain[0]
        return first_option.option_type

    def __init__(self,ticker='',expiration_date=None):
        assert ticker
        assert expiration_date
        self.ticker = ticker
        self.expiration_date = pd.Timestamp(expiration_date)
        self.__chain = []
    
    @staticmethod
    def from_list(chain=[],copy=True) -> object:
        assert len(chain) > 0
        fst = chain[0]
        assert type(fst) is Option
        this = ExpirationCycle(fst.ticker, fst.expiration_date)
        for option in chain:
            opt = Option(option.as_dict())
            this.chain.append(opt)
        
        if not this._validate():
            raise TypeError(f'{this.chain} is invalid.')
            
        return this
    
    @staticmethod
    def from_symbol_expiry_pair(ticker,date=None) -> object:
        exp_dates = list(live.get_expiration_dates(ticker)) if date is None else [ut.norm_date(date)]
        chain = list(map(Option,record_option_chains([ticker], [exp_dates[0]])))
        return ExpirationCycle.from_list(chain,copy=False) # Just constructed them. No need to copy.
        
        
    def _validate(self) -> bool:
        date = self.expiration_date
        for contract in self.chain:
            if not (contract.expiration_date == date and contract.ticker == self.ticker):
                return False
        return True
    
    @property
    def calls(self) -> list[Option]:
        def is_call(option):
            return option.option_type == 'CALL'
        return list(filter(is_call,self.chain))
    
    @property
    def puts(self) -> list[Option]:
        def is_put(option):
            return option.option_type == 'PUT'
        return list(filter(is_put,self.chain))
    
    def append_option(self,option: object) -> None:
        assert type(option) is Option
        self.chain.append(option)

    def export(self, exclude_keys=[]) -> list[dict[str, object]]:
        options = []
        for option in self.chain:
            in_the_money = option.in_the_money()
            opt_dic = {}
            for k, v in option.as_dict().items():
                if not k in exclude_keys:
                    opt_dic[k] = v
            if not 'in_the_money' in exclude_keys:
                opt_dic['in_the_money'] = in_the_money
            if not 'in_the_money_snapshot' in exclude_keys:
                opt_dic['in_the_money_snapshot'] = ut.now()
            
            options.append(opt_dic)
        return options

    def group_by_in_the_money(self) -> dict[str, list[object]]:
        group = {'in': [], 'out': []}
        for op in self.chain:
            if op.in_the_money():
                group['in'].append(op)
            else:
                group['out'].append(op)
        return group
    
    def __str__(self) -> str:
        chain = [op.as_dict() for op in self.chain]
        return pd.DataFrame(chain).to_string()
    
    def __repr__(self) -> str:
        itm_grouping = self.group_by_in_the_money()
        in_itm, out_itm = len(itm_grouping['in']), len(itm_grouping['out'])
        return '\n'.join([
            f'Option Expiration Cycle ({self.cycle_type})',
            f'Ticker: {self.ticker}',
            f'Expiration Date: {self.expiration_date.date()}',
            f'Contracts: {len(self.chain)}',
            f'Contracts (in: {in_itm}, out: {out_itm}) of the money'
        ])
