from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://microdata.worldbank.org/index.php/catalog/3902"
ORGANIZATION = "UNPS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_website_link'] = ORG_URL
    res['access_type'] = 'Open Access'
    res['sponsor_name'] = "Uganda Bureau of Statistics (UBOS)"
    res['dataset_name']="Uganda National Panel Survey (UNPS)"
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('div', attrs={'class':'field-metadata.study_desc.study_info.abstract'}).find(
        'div',attrs={'class':'field-value'}).get_text())
    res['about_info'] = about
    last_updated = 'April 21, 2021'
    res['last_updated'] = last_updated
    res['dataset_status'] = 'Retired' if is_older_than_5yrs(last_updated) else 'Active'
    return res

# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# for attribute, value in data_attributes.items():
#     print(f'{attribute}: {value}',end="\n\n")
# print()
# # print(data_attributes)