#!/usr/bin/python3

import json
import requests
import logging
from datetime import datetime

# from resources.endpoints import CPES_BASE_URL_V2, CVES_BASE_URL_V2

# save req and iso_dt to db

"""
As per NVD.NIST.GOV:
The CVE and CPE APIs are the preferred method for staying up to date with the NVD.
----------------
    CVE API
----------------
The CVE API is used to easily retrieve information on a single CVE or a collection of CVE 
from the NVD. The NVD contains more than 190,000 CVE. Because of this, its APIs enforce 
offset-based pagination to answer requests for large collections. Through a series of smaller “chunked” responses controlled by an offset 'startIndex' and a page limit 'resultsPerPage' users may page through all the CVE in the NVD.

    Important considerations:
        The best, most efficient, practice for keeping up to date with the NVD is to use the date range 
        parameters to request only the CVEs that have been modified since your last request.

        It is recommended that users of the CVE API use the default resultsPerPage value. 
        This value has been optimized to allow the greatest number of results over the fewest number of requests.

----------------
    CPE API
----------------
The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE records from the Official CPE Dictionary . The dictionary contains more than 860,000 CPE records and more than 408,000 match strings. Because of this, the NVD enforces offset-based pagination to answer requests for large collections. Through a series of smaller “chunked” responses controlled by an offset startIndex and a page limit resultsPerPage users may page through all the records in the dictionary. For more information on the full CPE specification please refer to NVD's Computer ecurity Resource Center.
"""

# TODO: There is a fair amount of refactoring to be done here that I likely will not get to by mid-day Friday.
# Most of should be pretty apparent. As for the rest, and for example:
# For flexibility, we can allow an argument to be passed to change API versions.
# The rest revolves around how clean the client itself is to work with. 

CVES_BASE_URL_V2 = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
CPES_BASE_URL_V2 = 'https://services.nvd.nist.gov/rest/json/cpes/2.0'

def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json_string = json.dumps(data)
        file.write(json_string)

"""API Wrapper for NVD Data APIs"""
class Nvd():

    def __init__(self):
        super().__init__()
        # self.api_version  = DEFAULT_API_VERSION
        self.cves_base_url  = CVES_BASE_URL_V2 # + DEFAULT_API_VERSION
        self.cpes_base_url  = CPES_BASE_URL_V2 # + DEFAULT_API_VERSION

    """
    CVE Vulnerabilities API
        NVD Web Documentation: https://nvd.nist.gov/developers/vulnerabilities

        TODOS
        - TODO: utility regex function to check for correct date formatting

        Params & Filters:
        ----
        resultsPerPage
            {page limit}
            Query Param: 'resultsPerPage='
        
            # This parameter specifies the maximum number of CVE records to be returned 
            # in a single API response. For network considerations, the default value and 
            # maximum allowable limit is 2,000.
        ----
        startIndex
            {offset}
            Query Param: 'startIndex='
            
            # This parameter specifies the index of the first CVE to be returned in the response data. 
            # The index is zero-based, meaning the first CVE is at index zero.
            #
            # The CVE API returns four primary objects in the response body that are used for pagination: 
                # resultsPerPage, startIndex, totalResults, and vulnerabilities. 
                    # totalResults indicates the total number of CVE records that match the request parameters. 
                    # If the value of totalResults is greater than the value of resultsPerPage, 
                    # there are more records than could be returned by a single API response and additional 
                    # requests must update the startIndex to get the remaining records.
            #
            # !! The best, most efficient, practice for keeping up to date with the NVD is to use the date range 
            # parameters to request only the CVEs that have been modified since your last request.
            #
            # It is recommended that users of the CVE API use the default resultsPerPage value. 
            # This value has been optimized to allow the greatest number of results over the fewest number of requests.
        cpeName
            {name}
            Query Param: 'cpeName='

            # This parameter returns all CVE associated with a specific CPE. 
            # The exact value provided with cpeName is compared against the 
            # CPE Match Criteria within a CVE applicability statement. If the 
            # value of cpeName is considered to match, the CVE is included in 
            # the results.
            #
            # A CPE Name is a string of characters comprised of 13 colon separated 
            # values that describe a product. In CPEv2.3 the first two values are 
            # always “cpe” and “2.3”. The 11 values that follow are referred to as 
            # the CPE components.
            #
            # CPE Match Criteria comes in two forms: CPE Match Strings and CPE Match 
            # String Ranges. Both are abstract concepts that are then correlated to CPE 
            # URIs in the Official CPE Dictionary. Unlike a CPE Name, match strings and 
            # match string ranges do not require a value in the part, vendor, product, 
            # or version components. The CVE API returns CPE Match Criteria within the 
            # configurations object.
        ----
        cveId
            {CVE-ID}
            Query Param: 'cveID='

            # This parameter returns a specific vulnerability identified by its unique 
            # Common Vulnerabilities and Exposures identifier (the CVE ID). cveId will 
            # not accept {CVE-ID} for vulnerabilities not yet published in the NVD.
        ----
        cvssV2Metrics
            {CVSSv2 vector string}
            Query Param: 'cvssV2Metrics='

            # This parameter returns only the CVEs that match the provided 
            # {CVSSv2 vector string}. Either full or partial vector strings may be used. 
            # This parameter cannot be used in requests that include cvssV3Metrics.
            #
            # Please note, as of July 2022, the NVD no longer generates new information 
            # for CVSS v2. Existing CVSS v2 information will remain in the database but 
            # the NVD will no longer actively populate CVSS v2 for new CVEs. 
            # NVD analysts will continue to use the reference information provided with 
            # the CVE and any publicly available information at the time of analysis to 
            # associate Reference Tags, information related to CVSS v3.1, CWE, and CPE 
            # Applicability statements.
        ----
        cvssV2Severity
            LOW | MEDIUM | HIGH
            Query Param: 'cvssV2Severity='

            # This parameter returns only the CVEs that match the provided CVSSv2 qualitative 
            # severity rating. This parameter cannot be used in requests that include cvssV3Severity.
            # 
            # Please note, as of July 2022, the NVD no longer generates new information for CVSS v2. 
            # Existing CVSS v2 information will remain in the database but the NVD will no longer 
            # actively populate CVSS v2 for new CVEs. NVD analysts will continue to use the reference 
            # information provided with the CVE and any publicly available information at the time of 
            # analysis to associate Reference Tags, information related to CVSS v3.1, CWE, and CPE 
            # Applicability statements.
        ----
        cvssV3Metrics
            {CVSSv3 vector string}
            Query Param: 'cvssV3Metrics='

            # This parameter returns only the CVEs that match the provided {CVSSv3 
            # vector string}. Either full or partial vector strings may be used. 
            # This parameter cannot be used in requests that include cvssV2Metrics.
        ----
        cvssV3Severity optional
            LOW | MEDIUM | HIGH | CRITICAL
            Query Param: 'cvssV3Severity='

            # This parameter returns only the CVEs that match the provided CVSSv3 
            # qualitative severity rating. This parameter cannot be used in requests 
            # that include cvssV2Severity.
        ----
        cweId
            {CWE-ID}
            Query Param: 'cweId='
            
            # This parameter returns only the CVE that include a weakness identified by 
            # Common Weakness Enumeration using the provided {CWE-ID}.
        ----
        hasCertAlerts
            *No Parameter Value*
            Query Param: 'hasCertAlerts='
            
            # This parameter returns the CVE that contain a Technical Alert from US-CERT. 
            # Please note, this parameter is provided without a parameter value.
        ----
        hasCertNotes 
            *No Parameter Value*
            Query Param: 'hasCertNotes='

            # This parameter returns the CVE that contain a Vulnerability Note from CERT/CC. 
            # Please note, this parameter is provided without a parameter value.
        ----
        hasKev
            *No Parameter Value*
            Query Param: 'hasKev='

            # This parameter returns the CVE that appear in CISA's Known Exploited Vulnerabilities 
            # (KEV) Catalog. Please note, this parameter is provided without a parameter value.
        ----
        hasOval
            *No Parameter Value*
            Query Param: 'hasOval='

            # This parameter returns the CVE that contain information from MITRE's Open Vulnerability 
            # and Assessment Language (OVAL) before this transitioned to the Center for Internet 
            # Security (CIS). Please note, this parameter is provided without a parameter value.
        ----
        isVulnerable *OPTIONAL FILTER*
            Filer Param: '&isVulnerable'

            # This parameter returns only CVE associated with a specific CPE, where the CPE is also 
            # considered vulnerable. The exact value provided with cpeName is compared against the 
            # CPE Match Criteria within a CVE applicability statement. If the value of cpeName is 
            # considered to match, and is also considered vulnerable the CVE is included in the results.
            #
            # If filtering by isVulnerable, cpeName is REQUIRED. Please note, virtualMatchString is 
            # not accepted in requests that use isVulnerable.
        ----
        keywordSearch
            {keyword(s)}
            Query Param: 'keywordSearch='

            # This parameter returns only the CVEs where a word or phrase is found in the current 
            # description. Please note, the descriptions associated with CVE are maintained by the 
            # CVE Assignment Team through coordination with CVE Numbering Authorities (CNAs). 
            # The NVD has no control over CVE descriptions.
            #
            # Please note, multiple {keywords} function like an 'AND' statement. This returns results 
            # where all keywords exist somewhere in the current description, though not necessarily together.
        ----
        keywordExactMatch OPTIONAL FILTER FOR keywordSearch
            Filter Param: '&keywordExactMatch'

            # By default, keywordSearch returns any CVE where a word or phrase is found in the current description.
            #
            # If the value of keywordSearch is a phrase, i.e., contains more than one term, including keywordExactMatch 
            # returns only the CVEs matching the phrase exactly. Otherwise, the results will contain records having any 
            # of the terms. If filtering by keywordExactMatch, keywordSearch is REQUIRED. Please note, this parameter 
            # is provided without a parameter value.
        ----
        lastModStartDate & lastModEndDate
            {start date} | {end date}
            Query Params: 'lastModStartDate=', 'lastModEndDate='

            # These parameters return only the CVEs that were last modified during the specified period. 
            # If a CVE has been modified more recently than the specified period, it will not be included in 
            # the response. If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED. 
            # The maximum allowable range when using any date range parameters is 120 consecutive days.
            #
            # A CVE is considered "modified" when any of the follow actions occur:
                # The NVD publishes the new CVE record
                # The NVD changes the status of a published CVE record
                # A source (CVE Primary CNA or another CNA) modifies a published CVE record
                # Values must be entered in the extended ISO-8061 date/time format:
                    # [YYYY][“-”][MM][“-”][DD][“T”][HH][“:”][MM][“:”][SS][Z]
                        # The "T" is a literal to separate the date from the time. The Z indicates an optional offset-from-UTC. 
                        # Please note, if a positive Z value is used (such as +01:00 for Central European Time) then the "+" 
                        # should be encoded in the request as "%2B". The user agent may handle this automatically.
        ----
        pubStartDate & pubEndDate
            {start date} | {end date}
            Query Params: 'startDate=', 'endDate='
            
            # These parameters return only the CVEs that were added to the NVD (i.e., published) 
            # during the specified period. If filtering by the published date, both lastModStartDate 
            # and lastModEndDate are REQUIRED. The maximum allowable range when using any date range 
            # parameters is 120 consecutive days.
                # Values must be entered in the extended ISO-8061 date/time format:
                    # [YYYY][“-”][MM][“-”][DD][“T”][HH][“:”][MM][“:”][SS][Z]
                        # The "T" is a literal to separate the date from the time. 
                        # The Z indicates an optional offset-from-UTC. 
                        # Please note, if a positive Z value is used (such as +01:00 for 
                        # Central European Time) then the "+" should be encoded in the request as "%2B". 
                        # The user agent may handle this automatically.
        ----
        sourceIdentifier
            {sourceIdentifier}
            Query Param: 'sourceIdentifier'

            # This parameter returns CVE where the exact value of {sourceIdentifier} appears as a data source 
            # in the CVE record. The CVE API returns {sourceIdentifier} values within the descriptions object. 
            # The Source API returns detailed information on the organizations that provide the data contained 
            # in the NVD dataset, including every valid {sourceIdentifier} value.
        ----
        virtualMatchString
            {cpe match string}
            Query Param: 'virtualMatchString='

            # This parameter filters CVE more broadly than cpeName. The exact value of {cpe match string} is 
            # compared against the CPE Match Criteria present on CVE applicability statements.
            #
            # CPE Match Criteria comes in two forms: CPE Match Strings and CPE Match String Ranges. 
            # Both are abstract concepts that are then correlated to CPE URIs in the Official CPE Dictionary. 
            # Unlike a CPE Name, match strings and match string ranges do not require a value in the part, 
            # vendor, product, or version components. The CVE API returns CPE Match Criteria within the 
            # configurations object.
            #
            # Please note, CPE Match String Ranges are not supported by the virtualMatchString. 
            # cpeName is a simpler alternative for many use cases. When both cpeName and virtualMatchString 
            # are provided, only the cpeName is used.
    """
    
    def get_all_cves_for_given_cpe_name(cpe_name):
        q = CVES_BASE_URL_V2 + '?cpeName=' + cpe_name

        res = requests.get(q)
        res_json = res.json()

        df = pd.json_normalize(res_json)

        write_json_to_file(res_json, f'{cpe_name}.json')

        print(df.head())

        # write_json_to_file(res_json, 'test.json')

        # df = pd.read_json(res_json)
        # print(df.to_json())
        # df.to_csv('../tmp/data/{self.cpe_name}_cves.csv', index = None)

    def search_cves_by_keyword(keyword):
        q = CVES_BASE_URL_V2 + '?keywordSearch=' + keyword

        res = requests.get(q)
        res_json = res.json()

        # df = pd.DataFrame(pd.json_normalize(res_json))

        # print(df.head())
        

        # write_json_to_file(res_json, f'{keyword}.json')

    def get_updated_cves():
        # get_last_cve_request
        pass

def iso_datetime():
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

# Nvd.search_cves_by_keyword('log4j')
Nvd.get_all_cves_for_given_cpe_name(
    "cpe:2.3:o:microsoft:windows_10:1607:*:*:*:*:*:*:*"
)
