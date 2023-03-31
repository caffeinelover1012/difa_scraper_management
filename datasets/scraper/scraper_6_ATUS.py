import requests
from bs4 import BeautifulSoup
from date_utils import *
from statics import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/"
ORGANIZATION = "ATUS"
SCRAPE_ID = 1
# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_website_link'] = 'https://www.bls.gov/tus/modules/ehdatafiles.htm'
    res['dataset_link'] = ORG_URL
    res['access_type'] = OPEN_ACCESS
    res['sponsor_name'] = "United States Department of Agriculture's Economic Research Service"
    res['dataset_name']="American Time Use Survey (ATUS) - Eating and Health Module (EHM)"
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('section', id='primary').find(
        'div').find_all('p')[1].get_text())
    res['about_info'] = about
    res['dataset_file_format']={'xlsx','csv'}
    table = soup.find('table', attrs={'class':'usa-table'}).find('tbody')
    rows = table.find_all('tr')[1]
    latest = (rows.find('td',attrs={'data-label':'Last Updated'}).get_text())
    res['last_updated'] = standardize(DATE_FMT, latest)
    res['dataset_status'] = 'Retired' if is_older_than_5yrs(res['last_updated']) else 'Active'
    return res

# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# # for attribute, value in data_attributes.items():
# #     print(f'{attribute}: {value}',end="\n\n")
# # print()
# print(data_attributes)
# # print(data_attributes)