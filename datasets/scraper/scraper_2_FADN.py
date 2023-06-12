from .common_imports import *
DATE_FMT = "%d.%m.%Y"
ORG_URL = "https://agriculture.ec.europa.eu/data-and-analysis/farm-structures-and-economics/fadn_en"
ORGANIZATION = "FADN"
DATASET_NAME = "Farm Accountancy Data Network (FADN)"
SPONSOR_NAME = "European Union"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):
    res = {i: "N/A" for i in ATTRS}
    res['acronym'] = "FADN"
    res['access_type'] = 'Open Access'
    res['sponsor_name'] = SPONSOR_NAME
    res['dataset_name'] = DATASET_NAME
    res['dataset_website_link'] = ORG_URL
    res['dataset_link'] = 'https://data.europa.eu/data/datasets/farm-accountancy-data-network-public-database?locale=en; https://agridata.ec.europa.eu/extensions/FADNPublicDatabase/FADNPublicDatabase.html'
    res['dataset_file_format'] = ['HTML','CSV','PDF','DOCX','JSON','ODT','RTF','XLS','XLSX','XML']
    res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n\
                            For example, the citation would look like:\n {res['sponsor_name']} (2019) Farm Accountancy Data Network Public Database [Data set].\
                            Retrieved from https://data.europa.eu/data/datasets/farm-accountancy-data-network-public-database?locale=en\n"
    
    ABOUT = "The Farm Accountancy Data Network (FADN) is an instrument for evaluating the income of agricultural holdings and the impacts of the Common Agricultural Policy. The concept of the FADN was launched in 1965, when Council Regulation 79/65 established the legal basis for the organisation of the network. It consists of an annual survey carried out by the Member States of the European Union. The services responsible in the Union for the operation of the FADN collect every year accountancy data from a sample of the agricultural holdings in the European Union. Derived from national surveys, the FADN is the only source of microeconomic data that is harmonised, i.e. the bookkeeping principles are the same in all countries. Holdings are selected to take part in the survey on the basis of sampling plans established at the level of each region in the Union. The survey does not cover all the agricultural holdings in the Union but only those which due to their size could be considered commercial."
    res['about_info'] = ABOUT

    DATASET_COLLECTION_METHOD = "The information collected annually in the Member States for each of the 80,000 FADN sample farms includes approximately 1000 variables and refers to: Physical and structural data (location, crop areas, livestock numbers, etc.). Economic and financial data (production value of the different crops, stocks, sales, purchases, production costs, assets, liabilities, production quotas and subsidies, etc.). Data is collected through a Liaison Agency in each Member State or nominated bodies. The sample in each Member State is stratified according to region, economic size and type of farming to ensure its representativeness. The FADN sample does, however, not cover all agricultural holdings, but only those which due to their size are considered to be commercial. The quality of data in FADN in terms of completeness and time consistency is one if its main strengths, since a sophisticated quality check is done regularly."
    res['dataset_collection_method'] = DATASET_COLLECTION_METHOD

    # response = requests.get("https://data.europa.eu/data/datasets/farm-accountancy-data-network-public-database?locale=en")
    # soup = BeautifulSoup(response.content, 'html.parser')
    # last_updated = soup.find('span',class_="d-inline-block").get_text()
    # print(last_updated)
    # res['last_updated'] = standardize(DATE_FMT,last_updated)
    # res['dataset_status'] = 'Inactive' if is_older_than_5yrs(res['last_updated']) else 'Active'
    # print(res['last_updated'])
    
    return res