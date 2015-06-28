#!/usr/bin/python

# Copyright (c) 2015, Tofig Suleymanov
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
#    BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests

class Zillow(object):

    def __init__(self, zws_id):
        self.zws_id = zws_id
        self.last_http_code = None
        self.last_zcode = None
        self.last_zmessage = None

    
    def get_search_results(self, address, citystatezip, rentzestimate = False):
        '''
        This method returns a dictionary of search results.
        See http://www.zillow.com/howto/api/GetSearchResults.htm details.
        '''
        p = {'zws-id' : self.zws_id, 'citystatezip' : citystatezip, 'address' :
                address, 'rentzestimate': rentzestimate}
        r = \
        requests.get("http://www.zillow.com/webservice/GetSearchResults.htm",
                params = p)
        self.last_http_code = r.status_code
        if r.status_code == 200:
            return self.parse_search_results(r.content)
        else:
            print "Error occured"

    def parse_search_results(self, response_xml):
        '''
        Parses xml output from get_search_results and returns a dictironary
        with key/values based on
        http://www.zillow.com/howto/api/GetSearchResults.htm
        '''
        from xml.etree import ElementTree
        root  = ElementTree.fromstring(response_xml)
        self.last_zcode = root.find('message').find('code').text
        self.last_zmessage = root.find('message').find('text').text
        if self.last_zcode > 0:
            return False
        r = root.find('response').find('results').find('result')
        data = {}
        data['zpid'] = r.find('zpid').text
        data['links'] = {}
        for link in r.findall('links'):
            data['links']['homedetails'] = link.find('homedetails').text
            data['links']['mapthishome'] = link.find('mapthishome').text
            data['links']['comparables'] = link.find('comparables').text
        data['address'] = {}
        for address in r.findall('address'):
            data['address']['street'] = address.find('street').text
            data['address']['zipcode'] = address.find('zipcode').text
            data['address']['city'] = address.find('city').text
            data['address']['state'] = address.find('state').text
            data['address']['latitude'] = address.find('latitude').text
            data['address']['longitude'] = address.find('longitude').text
        data['zestimate'] = {}
        data['zestimate']['valuationRange'] = {}
        for zestimate in r.findall('zestimate'):
            data['zestimate']['amount'] = zestimate.find('amount').text
            data['zestimate']['currency'] = zestimate.find('amount').attrib['currency']
            data['zestimate']['last-updated'] =\
            zestimate.find('last-updated').text
            data['zestimate']['valueChange'] = zestimate.find('valueChange').text
            for valuation_range in r.findall('valuationRange'):
                data['zestimate']['valuation_range']['low'] = \
                valuation_range.find('low').text
                data['zestimate']['valuation_range']['high'] = \
                valuation_range.find('high').text
            data['zestimate']['percentile'] = \
            zestimate.find('percentile').text
        data['region'] = r.find('localRealEstate').find('region').attrib['name']
        return data

    def get_last_zcode(self):
        return self.last_zcode

    def get_last_zmessage(self):
        return self.last_zmessage
