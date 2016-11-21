# Interacts with BitStamp's HTTP(S) API, documented here https://www.bitstamp.net/api/

# To run this you need to:
# 1) Sign up to BitStamp - https://www.bitstamp.net/
# 2) Get an API key https://www.bitstamp.net/account/security/api/ - this'll give you a private and a public key
# 3) Put your secret key in a file name 'bs.key' in the same folder as this file, you probably want to [chmod 400 bs.key]
# 4) Update BISTAMP_CUSTOMER_ID and BITSTAMP_PUBLIC_KEY with your customer ID (you can get this here https://www.bitstamp.net/account/balance/) and public key

# You will need to generate a key with the appropriate permissions. Getting the current price needs no key.

import sys, logging, requests, time, os, json
from datetime import datetime

# for generating authentication info for BitStamp
import hmac, hashlib

# URLs
URL_BTC_USD_PX      = "https://www.bitstamp.net/api/v2/ticker/btcusd/"
URL_BALANCE         = "https://www.bitstamp.net/api/v2/balance/"
URL_BITCOIN_ADDRESS = "https://www.bitstamp.net/api/bitcoin_deposit_address/"
URL_OPEN_ORDERS     = "https://www.bitstamp.net/api/v2/open_orders/btcusd/"
URL_BUY_LIMIT_ORDER = "https://www.bitstamp.net/api/v2/buy/btcusd/"

# Do we really call each of these URLs? True means we dummy, as in we do NOT call the real URL (used for testing)
DUMMY_PRIVATE_API_CALLS = {URL_BALANCE : False}

# Known error responses
ERROR_RESPONSES = {"API key not found" : "Check the API key, its probably wrong, hasn't ben actived etc. You can check at https://www.bitstamp.net/account/security/api/",
                   "No permission found" : "This means the API key being used doesn't have permission to call the URL, re-generate one with the right access here https://www.bitstamp.net/account/security/api/"}

ERROR_SLEEP_TIME_SECS = 10
ERROR_RETRY_LIMIT     = 10

# Magic numbers
BUY  = 0
SELL = 1

class BitStampHttpClient():

  def __init__(self, app_name, client_id, public_key, logger_level=logging.INFO):

    self.app_name    = app_name
    self.client_id   = client_id
    self.public_key  = public_key

    self.btc_usd_fee = None
    self.logger      = None

    self.init_logger(logger_level)

  def dummy_api_call(self, function):
    """ Allows an API call to be 'dummied' for testing. """
  
    if "balance" == function:
      DUMMY_PRIVATE_API_CALLS[URL_BALANCE] = True

    else:
      self.logger.error("Did not recognise the function passsed to dummy_api_call(): %s" % (function))

  def init_logger(self, level):

    log_file = os.path.join("log", "%s.log" % (self.app_name))

    if os.path.isfile(log_file):
      os.rename(log_file, os.path.join("log", "%s.%s.log" % (self.app_name, datetime.utcnow().strftime('%Y%m%d%H%M%S'))))

    self.logger = logging.getLogger(self.app_name)
    hdlr        = logging.FileHandler(log_file)
    formatter   = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    hdlr.setFormatter(formatter)
    self.logger.addHandler(hdlr) 
    self.logger.setLevel(level)

  def do_http_get(self, url):
 
    errors = 0
    data   = None

    while errors < ERROR_RETRY_LIMIT:

      try:
        resp = requests.get(url=url, timeout=15)
        data = json.loads(resp.text)
        self.logger.info("GET request came back successfully, full response is %s" % (data))
        break
      except NameError, ne:
        self.loggger.error("NameError sending HTTP GET:", ne)
      except:
        self.logger.error("Error with HTTP exchange" + str(sys.exc_info()[0]))
        time.sleep(ERROR_SLEEP_TIME_SECS)
        errors = errors + 1
        continue

    return data

  def do_http_post(self, url, parameters):
  
    response = requests.post(url, data = parameters)

    if response.status_code != 200:
      self.logger.error("Did not get 200 response back from request to %s with params of %s, response text was '%s'" % (url, parameters, response.text))

      if response.json()["reason"] == "API key not found":
        self.logger.info("The supplied API key appears to be wrong")

      return None
    else:
      json_payload = response.json()

      error_text = None
      try:
        error_text = json_payload["error"]
      except:
        pass

      if error_text:
        self.logger.error("Response had an error - %s" % (error_text))
  
        # See if we've hit it before, and know what it means / what we need to do next
        if error_text in ERROR_RESPONSES.keys():
          self.logger.info(ERROR_RESPONSES[error_text])
        return None

      else:
        self.logger.info("POST request came back successfully, full response is %s" % (json_payload))
        return json_payload

  def get_api_connection_details(self):
  
    if not os.path.isfile(".bs.key"):
       self.logger.error("No key file found, create .bs.key with private key")
       print "No key file found. You need to create a file called '.bs.key' in the same directory as this script as put your private BitStamp API key in it"
       sys.exit(1)

    key_file = open(".bs.key", "r")
    lines    = key_file.readlines()
    key_file.close()

    secret_key = lines[0].strip()

    current_time_ms = int(time.time() * 1000)
    nonce           = current_time_ms

    message   = "%s%s%s" % (nonce, self.client_id, self.public_key)
    signature = hmac.new(secret_key, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

    self.logger.info("Generated signature for nonce=%d : %s" % (nonce, signature))

    return ({"key" : self.public_key, "signature" : signature, "nonce" : nonce})

  def get_btc_usd_price(self):
   
    data = self.do_http_get(URL_BTC_USD_PX)
    return {"time" : datetime.utcnow(), "bid" : data['bid'], "ask" : data['ask'], "vwap" : data['vwap']}

  def get_fees(self, json):

    if self.btc_usd_fee == None:

      self.btc_usd_fee = float(json["btcusd_fee"]) / 100.0
   
      self.logger.info("The fee for trading BTC and USD is %f" % (self.btc_usd_fee * 100.0))

  def get_balance(self, currency = "usd"):

    if DUMMY_PRIVATE_API_CALLS[URL_BALANCE]:
      self.logger.info("Returning dummy balance of 100 and setting fee to 0.25")

      self.get_fees({"btcusd_fee" : "0.25"})
      return 100

    else:
    
      parameters = self.get_api_connection_details()
      response   = self.do_http_post(URL_BALANCE, parameters)

      if not response:
        return -1
      else:
        json_key_to_look_for = "%s_balance" % (currency.lower())

        value = response[json_key_to_look_for]
        self.logger.info("Extracted balanace for %s as %s" % (currency, value))

        float_value = float(value)
        self.logger.info("Converted to a float: %f" % (float_value))

        self.get_fees(response)

        return float_value

  def get_bitcoin_address(self):

    parameters = self.get_api_connection_details()
    response   = self.do_http_post(URL_BITCOIN_ADDRESS, parameters)

    if not response:
      return
    else:
      self.logger.info("Extracted bitcoin address as as %s" % (response))

  def get_open_orders(self, include_buys=True, include_sells=True):

    self.logger.info("Calling Bitstamp open orders function")

    parameters = self.get_api_connection_details()
    response   = self.do_http_post(URL_OPEN_ORDERS, parameters)

    if not response:
      self.logger.info("No response from bistamp on open orders request - probably means no orders")
      return []
    else:

      self.logger.info("Have a response from open orders request %s" % (response))

      if len(response) == 0:
        self.logger.info("No open orders")
        return []
      else:
        orders_to_return = []

        for order in response:
          if (order["type"] == BUY) and (include_buys):
            orders_to_return.append(order)
          elif (order["type"] == SELL) or (include_sells):
            orders_to_return.append(order)

        self.logger.info("After filtering on side, returning %d orders - %s" % (len(orders_to_return), orders_to_return))

        return orders_to_return 

  def place_buy_limit_order(self, amount=None, price=None, limit_price=None):

    self.logger.info("Received request to buy %.8f bitcoin at a price of %.8f, then sell at a price of %.8f" % (amount, price, limit_price))

    parameters = self.get_api_connection_details()

    # Bitstamp mandates no more than 8 dps, in future may want to explicitly control the rounding - c.f. limit_price below
    parameters["amount"]      = "%.8f" % (amount) 
    parameters["price"]       = str(price)

    # Again Bitstamp asks for no more than 2dps, in t his case we always want it to round up, hacky way  of doing that  is to add 0.005, for example:
    # 700.123 -> we want 700.13 instead of 700.12, 700.123 + 0.005 = 700.128 -> 700.13
    # something like 700.987, which we want to round to 700.99, will still work: 700.987 + 0.005 = 700.992 -> 700.99
    parameters["limit_price"] = "%.2f" % (limit_price + 0.005)

    self.logger.info("Limit price after rounding is %s" % (parameters["limit_price"]))

    self.logger.debug("Parameters for buy limit order request are %s" % (parameters))

    response   = self.do_http_post(URL_BUY_LIMIT_ORDER, parameters)

    if not response:
      self.logger.info("No response from bistamp on buy limit order request")
    else:
      self.logger.info("Have a response from buy limit order request: %s" % (response))
