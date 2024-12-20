from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.ers.usda.gov/data-products/foodaps-national-household-food-acquisition-and-purchase-survey/"
ORGANIZATION = "FoodAPS"
DATASET_NAME = "National Household Food Acquisition and Purchase Survey (FoodAPS)"
SPONSOR_NAME = "United States Department of Agriculture's Economic Research Service"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):
    
    res = {i: "N/A" for i in ATTRS}
    res['acronym'] = "FoodAPS"
    res['dataset_website_link'] = ORG_URL
    res['dataset_link'] = ORG_URL
    res['access_type'] = OPEN_ACCESS
    res['sponsor_name'] = SPONSOR_NAME
    res['dataset_name']= DATASET_NAME
    res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n\
        For example, the citation would look like: {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8"
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
    res['dataset_collection_method'] = "The survey collects information about\
                                        Quantities and expenditures for all at-home and away-from-home foods and beverages purchased and acquired from all sources by all household members over a seven-day period;\
                                        Eating occasions by all household members; Household characteristics, including income, program participation, non-food expenditures, food security, health status,\
                                        and diet and nutrition knowledge; and Household access to food, including location of purchase and distance to food stores and restaurants. \
                                        Nutrient information about purchased food as well as local retail environmental information were merged into the data set based on scanned barcodes, \
                                        product descriptions, and household locations."
    for i in row_idx:
        key = rows[i].find_all('a')[0].get_text().split()[0]
        val = standardize(DATE_FMT, rows[i].find_all(
            'td', attrs={'data-label': 'Last Updated'})[0].get_text())
        last_updated[key.lower()] = val
    res['last_updated'] = get_latest([date for date in last_updated.values()])
    res['dataset_status'] = 'Inactive' if is_older_than_5yrs(res['last_updated']) else 'Active'
    return res
