import datetime, glob, csv

# CONSTANTS
NOW         = datetime.datetime.utcnow()
A_DAY_AGO   = NOW - datetime.timedelta(days=1)
AN_HOUR_AGO = NOW - datetime.timedelta(days=0, hours=1)

# GLOBAL VARIABLES

# Historic prices
HISTORIC_BID_PX = []
HISTORIC_ASK_PX = []

def load_historic_prices_from_csv_files(date_filter=None):

  first_date = None
  last_date  = None

  for file_name in glob.glob('data/bitstamp_btc-usd_prices.*.csv'):
    
    with open(file_name, 'rb') as csv_file:

      print "Parsing %s" % (file_name)

      csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

      for row in csv_reader:

        if row[0] == "Time":
          continue # ignore the header
        
        try:
          date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")

          if date_filter:
            if date < date_filter:
#              print "Ignoring price quote from %s since it is laterr than %s" % (date, date_filter)
              continue

          if (first_date == None) or (date < first_date):
            first_date = date

          if (last_date == None) or (date > last_date):
            last_date = date

        except:
          print "ERROR - Could not parse date - %s" % (row[0][:-3])

        try:
          HISTORIC_BID_PX.append(float(row[1]))
          HISTORIC_ASK_PX.append(float(row[2]))
        except:
          print "ERROR - Couldn't parse line in CSV file: %s" % (row)

  if len(HISTORIC_BID_PX) <= 0 :
    print "Have no historic bid price information, date filter was %s" % (date_filter)
    sys.exit(1)

  if len(HISTORIC_ASK_PX) <= 0 :
    print "Have no historic ask price information, date filter was %s" % (date_filter)
    sys.exit(1)

  print "Found %d bid and %d ask prices between %s and %s" % (len(HISTORIC_BID_PX), len(HISTORIC_ASK_PX), first_date, last_date)

def analyse_historic_prices(prices):

  total = 0
  num   = len(prices)
  min   = -1.0
  max   = -1.0

  integer_frequency = {}

  for px in prices:
    total = total + px

    if min == -1.0:
      min = px
    elif px < min:
      min = px

    if max == -1.0:
      max = px
    elif px > max:
      max = px

    int_px = int(px)
    if int_px in integer_frequency.keys():
      integer_frequency[int_px] = integer_frequency[int_px] + 1
    else:
      integer_frequency[int_px] = 1

  avg_px = float(total / num)
  print "After analysing %d prices, avergage price is %f, minimum was %f and maximum was %f" % (num, avg_px, min, max)
  print "Frequency of rounded prices:"

  for key in sorted(integer_frequency):
    val = integer_frequency[key]
    print " - %d : %d" % (key, val)

def main():

  print "Loading historic prices from CSV"
  load_historic_prices_from_csv_files(A_DAY_AGO);

  print "Analysing Bid prices"
  analyse_historic_prices(HISTORIC_BID_PX)
  print "Analysing Ask prices"
  analyse_historic_prices(HISTORIC_ASK_PX)

if __name__ == "__main__":
  main()
