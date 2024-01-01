from .BaseScraper import *

DATE_FMT = "%d %B %Y"
ORG_URL = "https://www.teagasc.ie/rural-economy/rural-economy/national-farm-survey/"
ORGANIZATION = "NFS"
DATASET_NAME = "Irish National Farm Survey (NFS)"
DATASET_COLLECTION_METHOD = "The data collected cover all the key financial and physical indicators at farm level viz inventories, sales, purchases, costs, subsidies, liabilities, assets, cropping programme, yields etc.\n\nIn recent years the NFS has extended the range of data covered to the farm household, as the increased emphasis on rural development and viability of rural communities has placed greater emphasis on farm household data e.g. off-farm employment and income, farm inheritance, household composition, age structure etc. Additional data are also being collected regarding environmental issues.\n\nData is collected using laptop computers on a regular basis throughout the year by a team of trained Teagasc Research Technicians located throughout the country. The NFS has always been conducted to ensure total confidentiality of individual farmer’s data. A unique code is used to identify each farm thus ensuring that data cannot be linked to a particular farm."
SPONSOR_NAME = "Teagasc, the Irish Agriculture and Food Development Authority"
DATASET_LINK = "https://www.ucd.ie/issda/data/"
ABOUT = "The National Farm Survey (NFS) has been conducted by Teagasc on an annual basis since 1972. The survey is operated as part of the Farm Accountancy Data Network of the EU and fulfils Ireland’s statutory obligation to provide data on farm output, costs and income to the European Commission. A random, nationally representative sample, of between 1,000 and 1,200 farms depending on the year, is selected annually in conjunction with the Central Statistics Office (CSO). Each farm is assigned a weighting factor so that the results of the survey are representative of the national population of farms. Pigs and poultry systems are not represented because of the small number of farms in these systems. Co-operation in the survey is voluntary but the survey is supported by the main farming organisations. The success of the NFS is largely dependent on the voluntary co-operation of farmers in providing reliable and accurate data on their farm businesses."  
ISSDA_DATA_REQUEST_FORM = "https://www.ucd.ie/issda/t4media/ISSDA_Application_Research_V5.docx"
INFS_DATA_ACCESS_INFO = "To access the data, please complete a ISSDA Data Request Form for Research Purposes\n\nLink to download form:" + ISSDA_DATA_REQUEST_FORM + "\n\nsign it, and send it to ISSDA by email <issda@ucd.ie>.\n\nData will be disseminated on receipt of a fully completed, signed form. Incomplete or unsigned forms will be returned to the data requester for completion."
DATASET_REPORTS = "https://www.teagasc.ie/rural-economy/rural-economy/national-farm-survey/national-farm-survey-reports/"

OTHER_INFO = f"""Main Uses of this dataset: Financial, Research, Policy, Farm advice/benchmark performance, EU Farm Accountancy Data Network (FADN), National Data on Agriculture \n
       {INFS_DATA_ACCESS_INFO} \n 
        The dataset reports are available at {DATASET_REPORTS}."""

class INFS(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "INFS",
            'access_type': self.constants['OPEN_ACCESS'],
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_website_link': ORG_URL,
            'dataset_link': DATASET_LINK,
            'dataset_collection_method': DATASET_COLLECTION_METHOD,
            'dataset_file_format': ["pdf"],
            'about_info': ABOUT,
            'other_info': OTHER_INFO
        })
        self.soup = self.fetch_data_with_requests(ORG_URL)
        self.extract_data_attributes()
        self.finalize_additional_attributes()

    def extract_data_attributes(self):
        try:
            report_page_soup = self.fetch_data_with_requests(DATASET_REPORTS)
            latest_link = "https://www.teagasc.ie" + report_page_soup.find('article', class_="content-primary").find('a').get('href')
            latest_report_soup = self.fetch_data_with_requests(latest_link)

            last_updated = latest_report_soup.find('div', class_='publication-info').get_text().split('\n')[1].strip()
            last_updated_date = standardize(DATE_FMT, last_updated)
            self.res["last_updated"] = last_updated_date
            self.res['dataset_status'] = 'Inactive' if is_older_than_5yrs(self.res['last_updated']) else 'Active'
        except Exception as e:
            self.error_out(str(e), self.dataset_id)

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"


# ---------------------------------------------------
    # Old code for reference
# ---------------------------------------------------
# def get_data_attributes(url):
    
#     res = {i: "N/A" for i in ATTRS}


#     #Dataset Collection Method

#     #Citation Method
#     DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from {res['dataset_link']}\n"
#     res["dataset_citation"] = DATASET_CITATION


#     response = requests.get('https://www.teagasc.ie/rural-economy/rural-economy/national-farm-survey/national-farm-survey-reports/')
#     soup = BeautifulSoup(response.content,'html.parser')
    
#     latest_link = "https://www.teagasc.ie/" + soup.find('article',class_="content-primary").find('a').get('href')
    
#     # # Find the last updated date of data and compute if the last collected is not more than 5 years of duration.
#     response = requests.get(latest_link)
#     soup = BeautifulSoup(response.content,'html.parser')
#     last_updated = soup.find('div',class_='publication-info').get_text().split('\n')[1].strip()
#     last_updated_date = standardize(DATE_FMT,last_updated)
#     res["last_updated"] = last_updated_date

#     latest_year_available = int(last_updated.strip()[-4:])
#     current_date = date.today()
#     current_year = current_date.year
#     year_difference = int(current_year)-int(latest_year_available)
#     status = "Active"
#     if year_difference >= 5:
#         status = "Inactive"
#     res["dataset_status"] = status

#     return res