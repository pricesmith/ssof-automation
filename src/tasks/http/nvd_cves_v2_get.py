#!/usr/bin/python3

import requests
import logging

"""
CVE API

The CVE API is used to easily retrieve information on a single CVE or a collection of CVE 
from the NVD. The NVD contains more than 190,000 CVE. Because of this, its APIs enforce 
offset-based pagination to answer requests for large collections. Through a series of smaller 
“chunked” responses controlled by an offset 'startIndex' and a page limit 'resultsPerPage' users 
may page through all the CVE in the NVD.
"""

CVES_API_BASE_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

class NvdCvesV2Get():

    def __init__(
        self,
        cpe_name,
        *args, 
        **kwargs,
    ):
        super().__init__()
        self.cves_base_url  = CVES_API_BASE_URL
        self.cpe_name       = cpe_name
    
    def get_all_cves_for_given_cpe_name(self):
        q = CVES_API_BASE_URL + '?cpeName=' + self.cpe_name
        res = requests.get(q)
        print(res.status_code, res.json())


nvd_api = NvdCvesV2Get("cpe:2.3:o:microsoft:windows_10:1607:*:*:*:*:*:*:*")
nvd_api.get_all_cves_for_given_cpe_name()
