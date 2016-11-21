# This program will monitor the current price of buying BitCoins in USD on BitSatmp, and buy bitcoins if/when teh (current) price
# falls below a supplied delta from the 24 hour VWAP average price.

# To run this you will need a BitStamp API key with these permissions:
# - Account balance
# - Open orders
# - Buy limit order
# - Bitcoin deposit address

import sys, time, logging, datetime

from bitstamp_http_client import BitStampHttpClient
from secret_stuff import MY_BITSTAMP_ID, MY_PUBLIC_BITSTAMP_KEY

SLEEP_TIME_SECS = 5 # Note that we can't hit Bitsamp more than once per second (600 per 10 mins) or they will block the IP.

APP_NAME = "bitstamp_low_price_buyer"

USAGE = """
%s [options]

MANDATORY
  --amount-to-trade=int   - The maximum total value of orders to be placed in USD
  --max-orders=int        - The maximum number of orders to be placed
  --order-qty=int         - The per order value
  --price-delta=float     - How much must the current ask price differ from the average before an order is placed

OPTIONAL
  --secs-between-orders   - How long (in seconds) to wait between one order being filled and placing the next order. Default 60s."
  --profit-percentage     - How much profit to wait for per order. Default 1%% + fees (currently fees are 0.25%% per trade, total 0.5%%)

EXAMPLE

%s --amount-to-trade=100 --max-orders=10 --order-qty=10 --price-delta=0.01

""" % (APP_NAME, APP_NAME)

bitstamp_client = BitStampHttpClient(APP_NAME, MY_BITSTAMP_ID, MY_PUBLIC_BITSTAMP_KEY, logger_level=logging.DEBUG) 

# TODO change this back
# Foor now, pretend that balance is 100
bitstamp_client.dummy_api_call("balance")

# re-use the loggger in the client, bit of a hack
logger = bitstamp_client.logger

# User must specify these
amount_to_trade               = None
max_number_of_orders_to_place = None
per_order_quantity            = None
price_delta                   = None # how different should the current price differ from the avergae before plaving a BUY

# Defaulted
seconds_between_orders        = 60   # wait X seconds between one order being filled and placing another order
profit_percentage             = 0.01 

for argument in sys.argv[1:]:

  if argument.startswith("--amount-to-trade="):
    amount_to_trade = int(argument[18:])
  elif argument.startswith("--max-orders="):
    max_number_of_orders_to_place = int(argument[13:])
  elif argument.startswith("--order-qty="):
    per_order_quantity = int(argument[12:])
  elif argument.startswith("--price-delta="):
    price_delta = float(argument[14:])
  elif argument.startswith("--secs-between-orders="):
    seconds_between_orders = int(argument[22:])
  elif argument.startswith("--profit-percentage="):
    profit_percentage = float(argument[20:])
  else:
    print "ERROR - unrecognised option '%s'" % (argument)
    print USAGE
    sys.exit(1)

errors = False
if amount_to_trade == None:
  print "ERROR - must specify amount to trade"
  errors = True

if max_number_of_orders_to_place == None:
  print "ERROR - must specify maximum number of orders to place"
  errors = True

if per_order_quantity == None:
  print "ERROR - must specify per order quantity"
  errors = True

if price_delta == None:
  print "ERROR - must specify price delta"
  errors = True

if errors:
   print USAGE
   sys.exit(1)

print "Amount to Trade    %d" % (amount_to_trade)
print "Max # Orders       %d" % (max_number_of_orders_to_place)
print "Per Order Quantity %d" % (per_order_quantity)
print "Price Delta        %.2f%% (The current ask price must be this much less than the 24 hour VWap average before a buy order will be placed)" % (price_delta * 100)

print "Waiting %d seconds between orders" % (seconds_between_orders)
print "Waiting for a %f%% (+ fees) profit before selling" % (profit_percentage)

check_max_amount = per_order_quantity * max_number_of_orders_to_place

if check_max_amount > amount_to_trade:
  print "ERROR - order quantity x number of orders exceeds the amount to trade, it should  equal it. %d x %d != %d" % (per_order_quantity, max_number_of_orders_to_place, amount_to_trade)
  sys.exit(1)

# Check user's balance
user_balance = bitstamp_client.get_balance()

if user_balance < amount_to_trade:
  print "ERROR - Your balance is less than the amount to trade. %.8f < %d" % (user_balance, amount_to_trade)
  sys.exit(1)

# Main loop - keep checking the price and place an order when the price drops

outstanding_order  = False
time_of_last_order = None

orders_to_date     = []
counter            = 0
last_number_orders = 0

while orders_to_date < max_number_of_orders_to_place:

  now = datetime.datetime.utcnow()

  if outstanding_order:
    logger.info("There are outstanding orders, going to check the status of them")

    open_orders = bitstamp_client.get_open_orders(only_buys=True)

    if len(open_orders) > 0:
      logger.info("Orders are still open, going to sleep")
      time.sleep(SLEEP_TIME_SECS)
    else:
      outstanding_order = False

  elif (time_of_last_order != None and (now <  time_of_last_order + datetime.timedelta(days=0, hours=0, minutes=0, seconds=seconds_between_orders))):
    logger.info("Time of last order was less than %d seconds ago, going to sleep" % (seconds_between_orders))
    time.sleep(SLEEP_TIME_SECS)

  else:

    logger.debug("No outstanding orders, going to check the price")

    current_price = bitstamp_client.get_btc_usd_price()

    ask   = float(current_price['ask'])
    vwap  = float(current_price['vwap'])
    thold = vwap * (1.0 - price_delta)

    if ask < thold:
      logger.info("Current ask price (%f) is less than the VWAP (%f) minus delta (%f), going to place an order" % (ask, vwap, thold))

      price  = ask
      amount = per_order_quantity / price

      # once the buy is complete, Bitstamp API will automatically place a SELL order with limit_price as the price
      # In our case we want to make a profit
      multiplier  = (1 + (bitstamp_client.btc_usd_fee * 2) + profit_percentage)
      limit_price = ask * multiplier

      logger.debug("Caulculated limit price as %f: %f x (1 + (%f *2) + %f)" % (limit_price, ask, bitstamp_client.btc_usd_fee, profit_percentage))
      logger.debug("Caulculated limit price as %f: %f x %f" % (limit_price, ask, multiplier))

      logger.info("Going to place order for %f bitcoin at a price of %f, selling again at %f" % (amount, price, limit_price))

      orders_to_date.append({"qty_usd" : per_order_quantity, "qty_btc" : amount, "price_buy" : price, "price_sell" : limit_price, "time" : now})

      bitstamp_client.place_buy_limit_order(amount=amount, price=ask, limit_price=limit_price)

      outstanding_order  = True
      time_of_last_order = now

    else:
      logger.debug("Current ask price (%f) is not less than the VWAP (%f) minus delta (%f), going to sleep" % (ask, vwap, thold))
      time.sleep(SLEEP_TIME_SECS)

  if (counter > 10) or (last_number_orders > len(orders_to_date)):
    print "Placed %d orders so far: %s" % (len(orders_to_date), orders_to_date)
    counter = 0
    last_number_orders = len(orders_to_date)
  else:
    counter = counter + 1
