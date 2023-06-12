from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/"
ORGANIZATION = "ATUS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['acronym'] = "ATUS"
    res['dataset_website_link'] = 'https://www.bls.gov/tus/modules/ehdatafiles.htm'
    res['dataset_link'] = ORG_URL
    res['access_type'] = OPEN_ACCESS
    res['sponsor_name'] = "United States Department of Agriculture's Economic Research Service"
    res['dataset_name']="American Time Use Survey (ATUS) - Eating and Health Module (EHM)"
    res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']} [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8\n "
    
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('section', id='primary').find(
        'div').find_all('p')[1].get_text())
    res['about_info'] = about
    DATASET_COLLECTION_METHOD = "USDA’s Economic Research Service, along with its funding and technical assistance cosponsors—the Food and Nutrition Service (FNS) and the National Cancer Institute (NCI)—worked with the Bureau of Labor Statistics (BLS) and the Census Bureau to collect data for the 2014-16 Eating & Health Module (EH Module), a supplement to the American Time Use Survey (ATUS). The 2014-16 EH Module asks ATUS respondents about secondary eating—that is, eating while doing another activity; soft drink consumption; grocery shopping preferences and fast food purchases; meal preparation and food safety practices; food assistance participation; general health, height and weight, and exercise; and income."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD
    res['dataset_file_format']={'xlsx','csv'}
    table = soup.find('table', attrs={'class':'usa-table'}).find('tbody')
    rows = table.find_all('tr')[1]
    latest = (rows.find('td',attrs={'data-label':'Last Updated'}).get_text())
    res['last_updated'] = standardize(DATE_FMT, latest)
    res['dataset_status'] = 'Inactive' if is_older_than_5yrs(res['last_updated']) else 'Active'
    res['other_info'] = "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/module-questions/"
    return res