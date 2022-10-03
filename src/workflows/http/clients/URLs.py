"""@package URLs
    A Python3 class that allows access to all of the functionality in the
    NVD Vulnerability and Product APIs.

    This package attempts to stay on top of changes to the APIs and allow an
    easy to user iterface with the NVD APIs. It is very much a work in progress.
    PRs are encouraged. Proper development of this client will inform better decisions
    on future api clients.    
"""
from datetime import datetime

CVES_BASE_URL = 'https://services.nvd.nist.gov/rest/json/cves/'
CPES_BASE_URL = 'https://services.nvd.nist.gov/rest/json/cpes/'

class URLs:
    """ The URLs class will handle all of the URLs. The purpose of this class is
        to essentially store and serve all of the URL strings useful to the
        NVD APIs.

        There is no processing of the URLs or the URL parameters done in this class.
        All of that logic is handled in the NVD Client class.

        Note: I don't really feel this needs to be a class. Will do for now, however.
    """
    def __init__(self, version="2.0", response_format="json", *args, **kwargs):

        """ The URLs class constructor defines all of the URLs used by the API.
            When adding new API functionality the URL needs to be added here.
        """
        self.version    = version
        self.format     = response_format

        self.cve_base_url = f'{CVES_BASE_URL}{self.version}'
        self.cpe_base_url = f'{CPES_BASE_URL}{self.version}'

        """ CVE Vulnerabilities API
            NVD Web Documentation: https://nvd.nist.gov/developers/vulnerabilities

            Params & Filters:
        """

        self.cpe_name = 'cpeName'
        """ cpeName
                {name}
                Query Param: 'cpeName='

        This parameter returns all CVE associated with a specific CPE. 
        The exact value provided with cpeName is compared against the 
        CPE Match Criteria within a CVE applicability statement. If the 
        value of cpeName is considered to match, the CVE is included in 
        the results.
        
        A CPE Name is a string of characters comprised of 13 colon separated 
        values that describe a product. In CPEv2.3 the first two values are 
        always “cpe” and “2.3”. The 11 values that follow are referred to as 
        the CPE components.
        
        CPE Match Criteria comes in two forms: CPE Match Strings and CPE Match 
        String Ranges. Both are abstract concepts that are then correlated to CPE 
        URIs in the Official CPE Dictionary. Unlike a CPE Name, match strings and 
        match string ranges do not require a value in the part, vendor, product, 
        or version components. The CVE API returns CPE Match Criteria within the 
        configurations object.
        """

        self.cve_id = 'cveID'
        """ cveId
                {CVE-ID}
                Query Param: 'cveID='

        This parameter returns a specific vulnerability identified by its unique 
        Common Vulnerabilities and Exposures identifier (the CVE ID). cveId will 
        not accept {CVE-ID} for vulnerabilities not yet published in the NVD.
        """

        self.cvss_v2_metrics = 'cvssV2Metrics'
        """ cvssV2Metrics
                {CVSSv2 vector string}
                Query Param: 'cvssV2Metrics='

        This parameter returns only the CVEs that match the provided 
        {CVSSv2 vector string}. Either full or partial vector strings may be used. 
        This parameter cannot be used in requests that include cvssV3Metrics.
        
        Please note, as of July 2022, the NVD no longer generates new information 
        for CVSS v2. Existing CVSS v2 information will remain in the database but 
        the NVD will no longer actively populate CVSS v2 for new CVEs. 
        NVD analysts will continue to use the reference information provided with 
        the CVE and any publicly available information at the time of analysis to 
        associate Reference Tags, information related to CVSS v3.1, CWE, and CPE 
        Applicability statements.
        """

        self.cvss_vs_severity = 'cvssV2Severity'
        """ cvssV2Severity
                LOW | MEDIUM | HIGH
                Query Param: 'cvssV2Severity='

        This parameter returns only the CVEs that match the provided CVSSv2 qualitative 
        severity rating. This parameter cannot be used in requests that include cvssV3Severity.
        
        Please note, as of July 2022, the NVD no longer generates new information for CVSS v2. 
        Existing CVSS v2 information will remain in the database but the NVD will no longer 
        actively populate CVSS v2 for new CVEs. NVD analysts will continue to use the reference 
        information provided with the CVE and any publicly available information at the time of 
        analysis to associate Reference Tags, information related to CVSS v3.1, CWE, and CPE 
        Applicability statements.
        """

        self.keyword_search         = 'keyword'
        self.last_mod_start_date    = 'lastModStartDate'
        self.last_mod_end_date      = 'lastModEndDate'
        self.keyword_exact_match    = 'keywordExactMatch'
        self.virtual_match_string   = 'virtualMatchString'
        self.start_index            = 'startIndex'
        self.results_per_page       = 'resultsPerPage'





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
