import request
import logging

CPES_API_BASE_URL = 'https://services.nvd.nist.gov/rest/json/cpes/2.0'

class NvdCpesV2Get():

    def __init__(
        self,
        cpe_name,
        last_mod_start_date,
        last_mod_end_date,
        keyword_search,
        keyword_exact_match,
        virtual_match_string,
        start_index         = 1,
        results_per_page    = 100,
        *args, 
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.start_index            = start_index
        self.results_per_page       = results_per_page
        self.cpe_name               = cpe_name
        self.last_mod_start_date    = last_mod_start_date
        self.last_mod_end_date      = last_mod_end_date
        self.virtual_match_string   = virtual_match_string
    
    def get_all_cpes_for_given_cpe_name(cpe_name = ''):
        q = CPES_API_BASE_URL + '?cpeName=' + cpe_name
        res = requests.get(q)
        print(res.status_code, res.json())

get_all_cves_for_given_cpe_name('cpe:2.3:o:microsoft:windows_10:1607:*:*:*:*:*:*:*')