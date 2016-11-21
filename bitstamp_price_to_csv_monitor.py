import os, csv, datetime, sys, time
from bitstamp_http_client import BitStampHttpClient

SLEEP_TIME_SECS       = 10
ERROR_SLEEP_TIME_SECS = 10

previous_ask_prices = {}
previous_bid_prices = {}

csv_file_name = os.path.join("data", "bitstamp_btc-usd_prices.%s.csv" % (datetime.datetime.today().strftime('%Y%m%d')))
file_already_exists = False
if os.path.isfile(csv_file_name):
  file_already_exists = True

# Open up a csv file
csv_file = open(csv_file_name, "ab")
csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

if not file_already_exists:
  # one time write headers
  csv_writer.writerow(['Time', 'Bid', 'Ask'])

bitstamp_client = BitStampHttpClient("bitstamp_price_to_csv_monitor", None, None) # Don't need to supply client ID and key since getting price is a public function and doesn't need keys

while True:

  data = bitstamp_client.get_btc_usd_price()

  try:
    csv_writer.writerow(data)
    csv_file.flush()

  except:
    print "Error writing to CSV file" + str(sys.exc_info()[0])
    time.sleep(ERROR_SLEEP_TIME_SECS)
    errors = errors + 1

  time.sleep(SLEEP_TIME_SECS)
  errors = 0
