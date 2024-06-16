# NSEGPT
NSEGPT is like the CHATGPT which provides all the NSE listed stock data information including all the documents. fundamentals and stocj OHLC data.
# NSEGPT
NSEGPT is a Python package to fetch stock data from the NSE India website.

## Installation

```bash```
pip install NSEGPT

## USAGE
from nsefetcher import NSEFETCHER

fetcher = NSEFETCHER(["RELIANCE", "TCS"])
all_stock_data = fetcher.gather_all_data()
print(all_stock_data)

from nsegpt 

