from .common_imports import *
DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://agriculture.ec.europa.eu/data-and-analysis/farm-structures-and-economics/fadn_en"
ORGANIZATION = "FADN"
DATASET_NAME = "Farm Accountancy Data Network (FADN)"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):
    res = {i: "N/A" for i in ATTRS}
    res['access_type'] = 'Open Access'
    res['sponsor_name'] = "European Union"
    res['dataset_name'] = DATASET_NAME
    res['last_updated'] = standardize(DATE_FMT,'06/13/2019')
    res['dataset_status'] = 'Retired' if is_older_than_5yrs(res['last_updated']) else 'Active'
    res['dataset_website_link'] = ORG_URL
    res['dataset_link'] = 'https://data.europa.eu/data/datasets/farm-accountancy-data-network-public-database?locale=en'
    res['dataset_file_format'] = ['HTML','CSV']
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n Farm Accountancy Data Network Public Database. (2019). [Data set]. European Commission, Directorate-General for Agriculture and Rural Development. http://data.europa.eu/88u/dataset/farm-accountancy-data-network-public-database\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('div',attrs={'class':'ecl'}).find('p').get_text())
    res['about_info'] = about
    update_txt = str(requests.get(res['dataset_link']).content)
    # print(update_txt)
    return res


# # x = get_data_attributes(FOOD_APS_URL)
# # print(x)
# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# # print(data_attributes)
# for attribute, value in data_attributes.items():
#     print(f'{attribute}: {value}',end="\n\n")
# print()
