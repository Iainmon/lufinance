# Lufrano Financial Instrument Library `- lufinance`



```python
import lufinance as lf
from lufinance import utils as ut
from database import db

print(ut.now(), 'Scraping...')

tickers = ['AAPL', 'SPY', 'BABA', 'F']
chain_data = lf.record_option_chains(tickers)
chains = [lf.Option(ch) for ch in  chain_data]

if len(chains) > 0:
    db.options.insert_many(chains)
    stored = ut.df(db.options.find().sort('captured_at',-1).limit(10))
    print(ut.now(), stored)
else:
    print(ut.now(), 'API limit hit. Trying again in 10 minutes.')
```