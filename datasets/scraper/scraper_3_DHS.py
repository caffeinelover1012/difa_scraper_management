from .BaseScraper import *

DATE_FMT = "%d/%m/%Y"
ORG_URL = "https://dhsprogram.com/"
ORGANIZATION = "DHS"
DATASET_NAME = "Demographic Health Survey (DHS)"
SPONSOR_NAME = "United States Agency for International Development (USAID)"

class DHS(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "DHS",
            'access_type': self.constants['RESTRICTED_ACCESS'],
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_website_link': ORG_URL,
            'dataset_link': 'https://dhsprogram.com/data/available-datasets.cfm',
            'dataset_file_format': ["ASCII", "STATA (.dta,.do,.dct)", "SPSS (.sav,.sps)", "SAS (.sas,.sas7bdat)",".DBF",".MDB"]
            })


        # Fetch and process data for 'about_info' and 'last_updated'
        about_soup = self.fetch_data_with_requests(ORG_URL)
        current_year = datetime.now().year
        date_url = f"https://dhsprogram.com/methodology/survey-search.cfm?sendsearch=1&sur_status=Completed&YrFrom=1985&YrTo={current_year + 1}&crt=1&listgrp=2"
        date_soup = self.fetch_data_with_requests(date_url)
        self.extract_data_attributes(about_soup=about_soup, date_soup=date_soup)

        self.finalize_additional_attributes()


    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)
        about_soup = kwargs.get('about_soup')
        date_soup = kwargs.get('date_soup')
        try:
            # Extract 'about_info'
            overview = "Demographic and Health Surveys (DHS) are nationally-representative household surveys..."
            about = about_soup.find('h3', attrs={"class": 'HomeBanner__message-text'}).get_text()
            self.res['about_info'] = overview + " " + about

            # Extract 'last_updated'
            table = date_soup.find('table')
            rows = table.find_all('tr')

            latest_date_str = None
            latest_date = None

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if cols and len(cols) > 5:  # Ensure the row has the expected number of columns
                    fieldwork_dates = cols[5].get_text().strip()
                    if '-' in fieldwork_dates:
                        # Extract the end date of the fieldwork
                        end_date_str = fieldwork_dates.split('-')[-1].strip()
                        end_date_str = f"01/{end_date_str}"  # Assuming the first day of the month
                        end_date = datetime.strptime(end_date_str, "%m/%d/%Y")
                        if latest_date is None or end_date > latest_date:
                            latest_date = end_date
                            latest_date_str = end_date_str

            if latest_date_str:
                # Standardize and update the last_updated attribute
                standardized_date = standardize(self.scraper_date_format, latest_date_str)
                self.res["last_updated"] = standardized_date
                self.res["dataset_status"] = "Active"
            else:
                raise ValueError("No fieldwork dates found in the table.")

        except Exception as e:
            self.error_out(str(e), self.dataset_id)
        return None 

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"
        return None
        
# ---------------------------------------------------
    # Old code for reference
# ---------------------------------------------------
# # Define a function to get the data attributes for an organization
# def get_data_attributes(url):

#     res = {i: "N/A" for i in ATTRS}
#     res['acronym'] = "DHS"
#     res['dataset_name']="Demographic Health Survey (DHS)"
#     res['dataset_website_link'] = ORG_URL

#     DATASET_COLLECTION_METHOD = "The basic approach of The DHS Program is to collect data that are comparable across countries. To achieve this, standard model questionnaires have been developed, along with a written description of why certain questions or sections have been included. These model questionnaires—which have been reviewed and modified in each of the seven phases of The DHS Program—form the basis for the questionnaires that are applied in each country. Typically, a country is asked to adopt the model questionnaire in its entirety, but can add questions of particular interest. However, questions in the model can be deleted if they are irrelevant in a particular country. There are two types of DHS surveys:\
#                                 Standard DHS Surveys have large sample sizes (usually between 5,000 and 30,000 households) and typically are conducted about every 5 years, to allow comparisons over time.\
#                                 Interim DHS Surveys focus on the collection of information on key performance monitoring indicators but may not include data for all impact evaluation measures (such as mortality rates). These surveys are conducted between rounds of DHS surveys and have shorter questionnaires than DHS surveys. Although nationally representative, these surveys generally have smaller samples than DHS surveys. \
#                                 DHS surveys collect primary data using four types of Model Questionnaires. A Household Questionnaire is used to collect information on characteristics of the household's dwelling unit and characteristics of usual residents and visitors. It is also used to identify members of the household who are eligible for an individual interview. Eligible respondents are then interviewed using an Individual Woman's or Man's Questionnaire. The Biomarker Questionnaire is used to collect biomarker data on children, women, and men. For special information on topics that are not contained in the Model Questionnaires, optional Questionnaire Modules are available. Interviews are conducted only if the respondent provides voluntary informed consent. " 
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

#     res['access_type'] = 'Restricted Access'
#     res['sponsor_name'] = "United States Agency for International Development (USAID)"

#     res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8"
    
#     res['dataset_link'] = 'https://dhsprogram.com/data/available-datasets.cfm'
#     # Make a request to the organization's website
#     response = requests.get(url)
#     # Parse the HTML content of the response using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#     overview = "Demographic and Health Surveys (DHS) are nationally-representative household surveys that provide data for a wide range of monitoring and impact evaluation indicators in the areas of population, health, and nutrition. "
#     about = (soup.find('h3', attrs={"class":'HomeBanner__message-text'}).get_text())
#     res['about_info'] = overview + about
#     curr_date = date.today()
#     last_updated = str(curr_date.month)+'/'+str(curr_date.day)+'/'+str(curr_date.year)
#     last_updated_date=standardize(DATE_FMT,last_updated)
#     res["last_updated"]=last_updated_date
#     res["dataset_status"]= "Active"
#     res['dataset_file_format'] = ["ASCII", "STATA (.dta,.do,.dct)", "SPSS (.sav,.sps)", "SAS (.sas,.sas7bdat)",".DBF",".MDB"]
#     return res
