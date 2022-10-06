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

    ###########################################################################
    # Docs:                                                                   #
    # CVE | Vulnerabilities : https://nvd.nist.gov/developers/vulnerabilities #
    # CPE | Products        : https://nvd.nist.gov/developers/products        #
    ###########################################################################

    def __init__(self):
        self.cve_base_url       = f'{CVES_BASE_URL}{DEFAULT_VERSION}'
        self.cpe_base_url       = f'{CPES_BASE_URL}{DEFAULT_VERSION}'
        self.cpe_match_base_url = f'{CPE_MATCH_BASE_URL}{DEFAULT_VERSION}'

        self.cve_query_terms = {
            'cpe_name'               : 'cpeName',
            'cve_id'                 : 'cveId',
            'cwe_id'                 : 'cweId',
            'cvss_v2_metrics'        : 'cvssV2metrics',
            'cvss_v3_metrics'        : 'cvssV3metrics',
            'cvss_v2_severity'       : 'cvssV2Severity',
            'cvss_v3_severity'       : 'cvssV3Severity',
            'keyword_search'         : 'keywordSearch',
            'keyword_exact_match'    : 'keywordExactMatch',
            'has_cert_alerts'        : 'hasCertAlerts',
            'has_cert_notes'         : 'hasCertNotes',
            'has_kev'                : 'hasKev',
            'has_oval'               : 'hasOval',
            'is_vulnerable'          : 'isVulnerable',
            'keyword_search'         : 'keywordSearch',
            'keyword_exact_match'    : 'keywordExactMatch',
            'last_mod_start_date'    : 'lastModStartDate',
            'last_mod_end_date'      : 'lastModEndDate',
            'pub_start_date'         : 'pubStartDate',
            'pub_end_date'           : 'pubEndDate',
            'results_per_page'       : 'resultsPerPage',
            'start_index'            : 'startIndex',
        }

        self.cpe_query_terms = {
            'cpe_name_id'           : 'cpeNameId',
            'cpe_match_string'      : 'cpeMatchString',
            'match_criteria_id'     : 'matchCriteriaId',
            'keyword_search'        : 'keywordSearch',
            'keyword_exact_match'   : 'keywordExactMatch',
            'last_mod_start_date'   : 'lastModStartDate',
            'last_mod_end_date'     : 'lastModEndDate',
            'results_per_page'      : 'resultsPerPage',
            'start_index'           : 'startIndex',
        }

        self.cpe_match_query_terms = {
            'cve_id'                : 'cveId',
            'match_criteria_id'     : 'matchCriteriaId',
            'last_mod_start_date'   : 'lastModStartDate',
            'last_mod_end_date'     : 'lastModEndDate',
            'results_per_page'      : 'resultsPerPage',
            'start_index'           : 'startIndex',
        }

    def search_cves(
        self,
        cpe_name: str | None                = None,
        cve_id: str | None                  = None,
        cwe_id: str | None                  = None, # Common Weakness Enumeration
        cvss_v2_metrics: str | None         = None,
        cvss_v3_metrics: str | None         = None,
        cvss_v2_severity: str | None        = None,
        cvss_v3_severity: str | None        = None,
        source_identifier: str | None       = None, # 
        virtual_match_string: str | None    = None, # 
        has_cert_alerts: bool | None        = None, # This parameter returns the CVE that contain a Technical Alert from US-CERT. 
        has_cert_notes: bool | None         = None, # This parameter returns the CVE that contain a Vulnerability Note from CERT/CC. 
        has_kev: bool | None                = None, # This parameter returns the CVE that appear in CISA's Known Exploited Vulnerabilities (KEV) Catalog. 
        has_oval: bool | None               = None, # This parameter returns the CVE that contain information from MITRE's Open Vulnerability and Assessment Language (OVAL) before this transitioned to the Center for Internet Security (CIS).
        is_vulnerable: bool | None          = None, # This parameter returns only CVE associated with a specific CPE, where the CPE is also considered vulnerable. If filtering by isVulnerable, cpeName is REQUIRED. Please note, virtualMatchString is not accepted in requests that use isVulnerable.
        keyword_search: str | None          = None, # Please note, multiple {keywords} function like an 'AND' statement. This returns results where all keywords exist somewhere in the current description, though not necessarily together.
        keyword_exact_match: bool | None    = None, # By default, keywordSearch returns any CVE where a word or phrase is found in the current description. If filtering by keywordExactMatch, keywordSearch is REQUIRED. 
        last_mod_start_date: str | None     = None, # If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        last_mod_end_date: str | None       = None, # If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        pub_start_date: str | None          = None, # These parameters return only the CVEs that were added to the NVD (i.e., published) during the specified period. If filtering by the published date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        pub_end_date: str | None            = None, # These parameters return only the CVEs that were added to the NVD (i.e., published) during the specified period. If filtering by the published date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        results_per_page: int | None        = None,
        start_index: int | None             = None,
    ):

        kwargs = locals()
        print(kwargs)

        # Enforce or work around NVD API rules: # TODO: Check date lengths
        if kwargs['keyword_exact_match'] and not kwargs['keyword_search']:
            pass # return err | or apply default
        if kwargs['cvss_v2_metrics'] and kwargs['cvss_v3_metrics']:
            pass # return err | or apply default
        if kwargs['cvss_v2_severity'] and kwargs['cvss_v3_severity']:
            pass # return err | or apply default
        if kwargs['last_mod_start_date'] or kwargs['last_mod_end_date']:
            if not kwargs['last_mod_start_date'] or not kwargs['last_mod_end_date']:
                pass # return err | or apply default
        if kwargs['pub_start_date'] or kwargs['pub_end_date']:
            if not kwargs['pub_start_date'] or not kwargs['pub_end_date'] or \
            kwargs['last_mod_start_date'] or not kwargs['last_mod_end_date']:
                pass # return err | or apply default

        # Prep params 
        query_params = []
        for key in kwargs:
            if kwargs[key]:
                if type(kwargs[key]) is str or int:
                    query_params.append(f'{self.cve_query_terms[key]}={kwargs[key]}')

                if type(kwargs[key]) is bool and kwargs[key] is True:
                    query_params.append(f'{self.cve_query_terms[key]}')
        
        # Build params
        query_params_str = '?'
        for param in query_params:
            query_params_str += param

        return self.cve_base_url + query_params_str 
  
    def search_cpes(
        self,
        cpe_name_id: str            = None,
        cpe_match_string: str       = None,
        match_criteria_id: str      = None, 
        keyword_search: str         = None, # Please note, multiple {keywords} function like an 'AND' statement. This returns results where all keywords exist somewhere in the current description, though not necessarily together.
        keyword_exact_match: bool   = None, # By default, keywordSearch returns any CVE where a word or phrase is found in the current description. If filtering by keywordExactMatch, keywordSearch is REQUIRED. 
        last_mod_start_date: str    = None, # If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        last_mod_end_date: str      = None, # If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED. The maximum allowable range when using any date range parameters is 120 consecutive days.
        results_per_page: int       = None,
        start_index: int            = None,
    ):

        kwargs = locals()

    def search_cpe_match_criteria():
        pass


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


client = NVD()
client.search_cves()
