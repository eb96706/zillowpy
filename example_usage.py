#!/usr/bin/python


from modules.zillow import *

# Get your Zillow API key here:
# http://www.zillow.com/howto/api/APIOverview.htm?utm_source=email&utm_medium=email&utm_campaign==emo-apiregistration-api
#

ZWSID=''

#


z = Zillow(ZWSID)

data = z.get_search_results(citystatezip = 94301, address = '2101 Waverley Street, Palo Alto, California')


if data:
    print data
else:
    print '''[FATAL]: Could not get search results.
         Return code from API: {0}
         Returned message: {1}'''.format(z.get_last_zcode(), z.get_last_zmessage())
