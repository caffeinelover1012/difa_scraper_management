from .common_imports import *

DATE_FMT = "%B %d, %Y"
ORG_URL = "https://www.census.gov/programs-surveys/cps.html"
ORGANIZATION = "CPS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "Current Population Survey (CPS)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The CPS is administered by the Census Bureau using a probability selected sample of about 60,000 occupied households. The fieldwork is conducted during the calendar week that includes the 19th of the month. The questions refer to activities during the prior week; that is, the week that includes the 12th of the month. Households from all 50 states and the District of Columbia are in the survey for 4 consecutive months, out for 8, and then return for another 4 months before leaving the sample permanently. This design ensures a high degree of continuity from one month to the next (as well as over the year). The 4-8-4 sampling scheme has the added benefit of allowing the constant replenishment of the sample without excessive burden to respondents.\n\nThe CPS questionnaire is a completely computerized document that is administered by Census Bureau field representatives across the country through both personal and telephone interviews. Additional telephone interviewing is conducted from the Census Bureau’s two centralized collection facilities in Jeffersonville, Indiana and Tucson, Arizona.\n\nMore information can be found at: https://www.census.gov/programs-surveys/cps/technical-documentation/methodology.html"
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Sponsor Name
    SPONSOR_NAME = "US Census Bureau"
    res["sponsor_name"]=SPONSOR_NAME

    GENERAL_DATASET_SEARCH_TOOL_MDAT = "https://data.census.gov/mdat/#/"
    res["dataset_link"] = GENERAL_DATASET_SEARCH_TOOL_MDAT

    #Citation Method
    DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from {res['dataset_link']}\n"
    res["dataset_citation"] = DATASET_CITATION

    #Type of access to the dataset
    res["access_type"] = "Open Access"

    about_info = "The Current Population Survey (CPS) is one of the oldest, largest, and most well-recognized surveys in the United States.  It is immensely important, providing information on many of the things that define us as individuals and as a society – our work, our earnings, and our education. In addition to being the primary source of monthly labor force statistics, the CPS is used to collect data for a variety of other studies that keep the nation informed of the economic and social well-being of its people.  This is done by adding a set of supplemental questions to the monthly basic CPS questions.  Supplemental inquiries vary month to month and cover a wide variety of topics such as child support, volunteerism, health insurance coverage, and school enrollment.  Supplements are usually conducted annually or biannually, but the frequency and recurrence of a supplement depend completely on what best meets the needs of the supplement’s sponsor. The CPS data collection has been approved by the Office of Management and Budget (OMB Number 0607-0049).  Without this number, we could not conduct this survey."
    res["about_info"] = about_info

    cps_datasets = [{"Annual Social and Economic Supplements":"https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.html"},
                    {"Basic Monthly CPS":"https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html"},
                    {"CPS Basic Extraction Files":"https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic-extractions.html"},
                    {"CPS Certification Items Extract Files":"https://www.census.gov/data/datasets/time-series/demo/cps/cps-cert.html"},
                    {"CPS Supplement and Replicate Weights":"https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt.html"}]

    res["other_info"] = cps_datasets 

    res["dataset_file_format"] = ["csv","pdf","sas","txt"]

    #Go to Basic Monthly CPS data release plan to see the latest data
    response = requests.get('https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html')
    soup = BeautifulSoup(response.content,'html.parser')

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available = soup.find('ul',id="list-tab-1979780401").find('a').get_text()
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    #Find when the dataset was last updated
    last_updated = soup.find('div',id="lastModifiedDiv").get_text()
    
    last_updated_date=standardize(DATE_FMT,last_updated[20:].strip())
    res["last_updated"]=last_updated_date

    return res