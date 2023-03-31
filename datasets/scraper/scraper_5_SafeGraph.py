import requests
from bs4 import BeautifulSoup
from date_utils import *
from statics import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.safegraph.com/"
ORGANIZATION = "SafeGraph"

# Define a function to get the data attributes for an organization

def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_website_link'] = ORG_URL
    res['access_type'] = 'Paid Access'
    res['last_updated'] = "Monthly"
    res['sponsor_name'] = "SafeGraph"
    res['dataset_name'] = "[Dataset Name]"
    res['dataset_link'] = "https://docs.safegraph.com/docs/bulk-data-delivery"
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from [source]\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    # Make a request to the organization's website
    response = requests.get("https://docs.safegraph.com/docs/open-census-data")
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    updateText = soup.find('div', attrs={'id': 'updated-at'}).getText()
    last_update = is_older_than_5_yrs_str(updateText)
    if last_update == True:
        res['dataset_status'] = 'Retired'
    else:
        res['dataset_status'] = 'Active'
    about = """SafeGraph is a data company that collects and provides datasets related to location-based analytics. The SafeGraph dataset contains anonymized data on foot traffic patterns at various locations, such as businesses, points of interest, and residential areas. The dataset includes information on the number of visitors to these locations, the duration of their visits, and other relevant data points. SafeGraph is narrowly focused on building the most accurate global places dataset available, empowering modern builders to create world-class location-based applications and analytics tools."""
    res['about_info'] = about
    formats = {'CSV': None, 'JSON': None, 'Parquet': None}
    res['dataset_file_format'] = list(formats.keys())
    return res


# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# for attribute, value in data_attributes.items():
#     print(f'{attribute}: {value}', end="\n\n")
# print()
# # print(get_data_attributes(SAFEGRAPH_URL))
