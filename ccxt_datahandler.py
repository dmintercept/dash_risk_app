import ccxt
from datetime import datetime, timedelta, timezone
import math
import pandas as pd
import datetime

def ccxt_datahandler(pair, exchange, timeframe):
	
	try:
		exchange = getattr (ccxt, exchange) ()
	except AttributeError:
		print('-'*36,' ERROR ','-'*35)
		print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange))
		print('-'*80)
		quit()
	 
	# Check if fetching of OHLC Data is supported
	if exchange.has["fetchOHLCV"] != True:
		print('-'*36,' ERROR ','-'*35)
		print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange))
		print('-'*80)
		quit()
	 
	# Check requested timeframe is available. If not return a helpful error.
	if (not hasattr(exchange, 'timeframes')) or (timeframe not in exchange.timeframes):
		print('-'*36,' ERROR ','-'*35)
		print('The requested timeframe ({}) is not available from {}\n'.format(timeframe,exchange))
		print('Available timeframes are:')
		for key in exchange.timeframes.keys():
			print('  - ' + key)
		print('-'*80)
		quit()
	 
	# Check if the symbol is available on the Exchange
	exchange.load_markets()
	if pair not in exchange.symbols:
		print('-'*36,' ERROR ','-'*35)
		print('The requested symbol ({}) is not available from {}\n'.format(pair,exchange))
		print('Available symbols are:')
		for key in exchange.symbols:
			print('  - ' + key)
		print('-'*80)
		quit()

	# Get data and convert df to usable format
	data = exchange.fetch_ohlcv(pair, timeframe, since=0)
	header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
	df = pd.DataFrame(data, columns=header).set_index('Timestamp')
	df.index = pd.to_datetime(df.index,unit='ms')
	return df

def parse_args():
	parser = argparse.ArgumentParser(description='CCXT Market Data Downloader')
 
	parser.add_argument('-s','--symbol',
						type=str,
						required=True,
						help='The Symbol of the Instrument/Currency Pair To Download')
 
	parser.add_argument('-e','--exchange',
						type=str,
						required=True,
						help='The exchange to download from')
 
	parser.add_argument('-t','--timeframe',
						type=str,
						default='1d',
						choices=['1m', '5m','15m', '30m','1h', '2h', '3h', '4h', '6h', '12h', '1d', '1M', '1y'],
						help='The timeframe to download')
 
	parser.add_argument('-w','--write',
						type=bool,
						required=True,
						help=('Option to write to file'))
	parser.add_argument('--debug',
						action ='store_true',
						help=('Print Sizer Debugs'))
 
	return parser.parse_args()