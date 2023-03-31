import requests
from bs4 import BeautifulSoup
from date_utils import *
from statics import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.ers.usda.gov/data-products/foodaps-national-household-food-acquisition-and-purchase-survey/"
ORGANIZATION = "FoodAPS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_website_link'] = ORG_URL
    res['dataset_link'] = ORG_URL
    res['access_type'] = OPEN_ACCESS
    res['sponsor_name'] = "United States Department of Agriculture's Economic Research Service"
    res['dataset_name']="National Household Food Acquisition and Purchase Survey (FoodAPS)"
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('section', id='primary').find(
        'div').find('p').get_text())
    res['about_info'] = about
    table = soup.find('table', class_='usa-table')
    rows = table.find_all('tr')
    last_updated = {'sas': None, 'stata': None, 'csv': None}
    res['dataset_file_format'] = list(last_updated.keys())
    row_data = ""
    row_idx = []
    for idx, row in enumerate(rows):
        cols = row.find_all('td')
        for col in cols:
            if col.find('a') is not None:
                row_data = (col.find('a').get_text())
                if "data files" in row_data:
                    row_idx.append(idx)

    for i in row_idx:
        key = rows[i].find_all('a')[0].get_text().split()[0]
        val = standardize(DATE_FMT, rows[i].find_all(
            'td', attrs={'data-label': 'Last Updated'})[0].get_text())
        last_updated[key.lower()] = val
    res['last_updated'] = get_latest([date for date in last_updated.values()])
    res['dataset_status'] = 'Retired' if is_older_than_5yrs(res['last_updated']) else 'Active'
    return res

# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# for attribute, value in data_attributes.items():
#     print(f'{attribute}: {value}',end="\n\n")
# print()
# # print(data_attributes)