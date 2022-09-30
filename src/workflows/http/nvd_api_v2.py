#!/usr/bin/python3

import requests
import logging

from resources.endpoints import CPES_BASE_URL_V2, CVES_BASE_URL_V2

# There's a good bit of refactoring that can and probably should be done here that I likely 
# will not get to by mid-day Friday.

"""
As per nvd.nist.gov:
The CVE and CPE APIs are the preferred method for staying up to date with the NVD.
---------------
    CVE API
---------------
The CVE API is used to easily retrieve information on a single CVE or a collection of CVE 
from the NVD. The NVD contains more than 190,000 CVE. Because of this, its APIs enforce 
offset-based pagination to answer requests for large collections. Through a series of smaller 
“chunked” responses controlled by an offset 'startIndex' and a page limit 'resultsPerPage' users 
may page through all the CVE in the NVD.
---------------
    CPE API
---------------
The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE 
records from the Official CPE Dictionary . The dictionary contains more than 860,000 CPE records 
and more than 408,000 match strings. Because of this, the NVD enforces offset-based pagination to 
answer requests for large collections. Through a series of smaller “chunked” responses controlled 
by an offset startIndex and a page limit resultsPerPage users may page through all the records in 
the dictionary. For more information on the full CPE specification please refer to the Computer 
Security Resource Center.
"""

# API Wrapper for nvd.nist.gov data apis
class NvdAPI_v2():

    def __init__(self):
        super().__init__()
        self.cves_base_url = CVES_BASE_URL_V2
        self.cpes_base_url = CPES_BASE_URL_V2

class CveAPI_v2(NvdAPI_v2):

    def __init__(self);
    
    def get_all_cves_for_given_cpe_name(self):
        q = CVES_BASE_URL_V2 + '?cpeName=' + self.cpe_name
        res = requests.get(q)
        print(res.status_code, res.json())


nvd_api = NvdCvesV2Get("cpe:2.3:o:microsoft:windows_10:1607:*:*:*:*:*:*:*")
nvd_api.get_all_cves_for_given_cpe_name()
