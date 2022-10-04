""" 
This implementation currently uses nested classes to leverage outer classes as 
as namespaces-- ideally for developer friendliness. 
"""

from datetime import datetime

CVES_BASE_URL       = 'https://services.nvd.nist.gov/rest/json/cves/'
CPES_BASE_URL       = 'https://services.nvd.nist.gov/rest/json/cpes/'
CPE_MATCH_BASE_URL  = 'https://services.nvd.nist.gov/rest/json/cpematch/'

DEFAULT_VERSION = '2.0'
DEFAULT_FORMAT  = 'json'

class NVD(object):
    def __init__(self):
        self.cpe_name               = 'cpeName'
        self.cve_id                 = 'cveID'
        self.cvss_v2_metrics        = 'cvssV2Metrics'
        self.cvss_vs_severity       = 'cvssV2Severity'
        self.keyword_search         = 'keyword'
        self.last_mod_start_date    = 'lastModStartDate'
        self.last_mod_end_date      = 'lastModEndDate'
        self.keyword_exact_match    = 'keywordExactMatch'
        self.virtual_match_string   = 'virtualMatchString'
        self.start_index            = 'startIndex'
        self.results_per_page       = 'resultsPerPage'

    class CPE(object):
        class Search(object):
            def __init__(self):
                self.q = f'{CPES_BASE_URL}{DEFAULT_VERSION}'

                self.cpe_name_id                = 'cpeNameId'
                self.cpe_match_string           = 'cpeMatchString'
                self.cpe_keyword_search         = 'keywordSearch'
                self.cpe_keyword_exact_match    = 'keywordExactMatch'

            def by_cpe_name_id(self, cpe_name_id):
                self.q += f'?{self.cpe_name_id}={cpe_name_id}'
                
            def by_cpe_match_string(self, cpe_match_string):
                self.q = f'?{self.cpe_match_string}={cpe_match_string}'

            def by_keyword(self, keyword):
                self.q = f'?{self.cpe_keyword_search}={keyword}'

            def by_keyword_exact_match(self, keyword):
                self.q = f'?{self.cpe_keyword_search}={keyword}&{self.cpe_keyword_exact_match}'

            def set_search_params():
                pass

    class CVE(object):
        class Search(object):
            def __init__(self):
                self.q = f'{CPES_BASE_URL}{DEFAULT_VERSION}'

                self.cpe_name                   = 'cpeName'
                self.cve_id                     = 'cveId'
                self.cpe_keyword_search         = 'keywordSearch'
                self.cpe_keyword_exact_match    = 'keywordExactMatch'

            def by_cpe_name_id(self, cpe_name_id):
                self.q += f'?{self.cpe_name_id}={cpe_name_id}'
                
            def by_cpe_match_string(self, cpe_match_string):
                self.q = f'?{self.cpe_match_string}={cpe_match_string}'

            def by_keyword(self, keyword):
                self.q = f'?{self.cpe_keyword_search}={keyword}'

            def by_keyword_exact_match(self, keyword):
                self.q = f'?{self.cpe_keyword_search}={keyword}&{self.cpe_keyword_exact_match}'

            def set_search_params():
                pass


    def _wrap_query_key(query_key):
        return f'?{query_key}='

    def _iso_datetime():
        """
        NVD datetimes support only ISO 8601 formats with microsecond precision to three decimal places
        """
        precision = 3
        iso_dt = datetime.now().isoformat('T')
        us = str(iso_dt.microsecond)
        f = us[:precision] if len(us) > precision else us
        return "%d-%d-%d %d:%d:%d.%d" % (
            iso_dt.year, iso_dt.month, iso_dt.day, iso_dt.hour, iso_dt.minute, iso_dt.second, int(f)
        )








    # def cves_by_cpe_name(self):
    # """Combines the request endpoint and accounts API URLs
    #     @param self - the object pointer
    # """
    # return self.base_url + self.cpe_name_query

    # def cves_by_keyword_search(self):
