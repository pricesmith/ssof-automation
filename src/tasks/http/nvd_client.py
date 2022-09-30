#!/usr/bin/python3

import requests
import pandas as pd
import logging
# import vcrpy
# import pytest

"""
As per NVD.NIST.GOV:
The CVE and CPE APIs are the preferred method for staying up to date with the NVD.
----------------
    CVE API
----------------
The CVE API is used to easily retrieve information on a single CVE or a collection of CVE 
from the NVD. The NVD contains more than 190,000 CVE. Because of this, its APIs enforce 
offset-based pagination to answer requests for large collections. Through a series of smaller “chunked” responses controlled by an offset 'startIndex' and a page limit 'resultsPerPage' users may page through all the CVE in the NVD.
----------------
    CPE API
----------------
The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE records from the Official CPE Dictionary . The dictionary contains more than 860,000 CPE records and more than 408,000 match strings. Because of this, the NVD enforces offset-based pagination to answer requests for large collections. Through a series of smaller “chunked” responses controlled by an offset startIndex and a page limit resultsPerPage users may page through all the records in the dictionary. For more information on the full CPE specification please refer to NVD's Computer ecurity Resource Center.
"""

# TODO: There is a fair amount of refactoring to be done here that I likely will not get to by mid-day Friday.
# Most of should be pretty apparent. As for the rest, and for example:
# For flexibility, we can allow an argument to be passed to change API versions.
# The rest revolves around how clean the client itself is to work with. 

# CVE and CPE API Base URLs respectively.
CVES_BASE_URL_V2 = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
CPES_BASE_URL_V2 = 'https://services.nvd.nist.gov/rest/json/cpes/2.0'

# API Wrapper for NVD data apis
class Nvd():

    def __init__(self):
        super().__init__()
        # self.api_version  = DEFAULT_API_VERSION
        self.cves_base_url  = CVES_BASE_URL_V2 # + DEFAULT_API_VERSION
        self.cpes_base_url  = CPES_BASE_URL_V2 # + DEFAULT_API_VERSION

    # 
    
    def get_all_cves_for_given_cpe_name(cpe_name):
        q = CVES_BASE_URL_V2 + '?cpeName=' + cpe_name
        res = requests.get(q)
        df = pd.read_json(res.json())
        df.to_csv('../data/{self.cpe_name}_cves.csv', index = None)



nvd_api = Nvd.get_all_cves_for_given_cpe_name(
    "cpe:2.3:o:microsoft:windows_10:1607:*:*:*:*:*:*:*"
)
