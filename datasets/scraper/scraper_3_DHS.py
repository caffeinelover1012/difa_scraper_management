from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://dhsprogram.com/"
ORGANIZATION = "DHS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_website_link'] = ORG_URL
    res['access_type'] = 'Open Access'
    res['sponsor_name'] = "United States Agency for International Development (USAID)"
    res['dataset_name']="Demographic Health Survey (DHS)"
    res['dataset_link'] = 'https://dhsprogram.com/data/available-datasets.cfm'
    res['dataset_citation'] = f"To cite the {res['dataset_name']} dataset in APA format in your research paper, you can use the following citation format:\n{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\nFor example, in your reference list, the citation would look like this:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8\n Make sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    about = (soup.find('h3', attrs={"class":'HomeBanner__message-text'}).get_text())
    res['about_info'] = about
    last_updated = {'sas': None, 'stata': None, 'spss': None,'ascii':None}
    res['dataset_file_format'] = list(last_updated.keys())
    return res
