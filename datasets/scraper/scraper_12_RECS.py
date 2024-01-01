from .BaseScraper import *

DATE_FMT = "%d %B %Y"
ORG_URL = "https://www.eia.gov/consumption/residential/"
ORGANIZATION = "RECS"
DATASET_NAME = "Residential Energy Consumption Survey (RECS)"
DATASET_COLLECTION_METHOD = "The Household Survey, a voluntary survey, collects data on energy-related characteristics and usage patterns of a national and sub-national (e.g., states) representative sample of housing units. The Energy Supplier Survey (ESS), a mandatory data collection, collects data on how much electricity, natural gas, propane/LPG, and fuel oil/kerosene were consumed in the sampled housing units during the reference year. The ESS also collects data on actual dollar amounts spent on these energy sources. EIA uses models (energy engineering-based models in the 2015 and 2020 survey) to produce consumption and expenditures estimates for heating, cooling, refrigeration, and other end uses in all housing units occupied as a primary residence in the United States using the data collected from the Household Survey and ESS. Wood-use estimates are also included as part of RECS. The target population for the RECS is all occupied housing units in the 50 states and the District of Columbia (DC) that are used as primary residences. The 2020 RECS introduced a completely self-administered design via web and paper questionnaire."
SPONSOR_NAME = "U.S. Energy Information Administration (EIA), a statistical agency of the U.S. Department of Energy"
ABOUT= "EIA administers the Residential Energy Consumption Survey (RECS) to a nationally representative sample of housing units. Traditionally, specially trained interviewers collect energy characteristics on the housing unit, usage patterns, and household demographics. For the 2020 survey cycle, EIA used Web and mail forms to collect detailed information on household energy characteristics. This information is combined with data from energy suppliers to these homes to estimate energy costs and usage for heating, cooling, appliances and other end uses — information critical to meeting future energy demand and improving efficiency and building design.\n\nFirst conducted in 1978, the fifteenth RECS collected data from nearly 18,500 households in housing units statistically selected to represent the 123.5 million housing units that are occupied as a primary residence. Data from the 2020 RECS are tabulated by geography and for particularly characteristics, such as housing unit type and income, that are of particular interest to energy analysis.\n\nThe results of each RECS include data tables, a microdata file, and a series of reports. Data tables are generally organized across two headings; 'Household Characteristics' and 'Consumption & Expenditures.'"

class RECS(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "RECS",
            'dataset_website_link': ORG_URL,
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_collection_method': DATASET_COLLECTION_METHOD,
            # Dataset link will be set after fetching the actual link
            'dataset_file_format': ["pdf", "xls", "zip"],
            'about_info': ABOUT,
            # Other info will be added after fetching additional data
        })
        
        self.main_page_soup = self.fetch_data_with_requests(ORG_URL)
        self.extract_data_attributes(main_page_soup=self.main_page_soup)
        self.finalize_additional_attributes()

    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)
        main_page_soup = kwargs.get('main_page_soup')

        try:
            # Fetch the dataset link from the main page
            dataset_link = "https://www.eia.gov/" + main_page_soup.find('li', class_="dropdown").find('a').get('href')
            self.res["dataset_link"] = dataset_link

            microdata_page = dataset_link + "/index.php?view=microdata"
            microdata_soup = self.fetch_data_with_requests(microdata_page)
            # Check if it matches "Month Year" format and handle accordingly
            last_updated_text = microdata_soup.find('table', class_='basic_table').find_all('td')[-1].get_text()
            if re.match(r"^[A-Z][a-z]+ \d{4}$", last_updated_text):  # Regex pattern for "Month Year"
                last_updated = f"1 {last_updated_text}"  # Prepend "1" to make it "1 Month Year"
                self.res["last_updated"] = standardize(DATE_FMT, last_updated)
            else:
                raise ValueError("Date format does not match expected 'Month Year' format from source date soup.")

            self.res['dataset_status'] = 'Inactive' if is_older_than_5yrs(self.res["last_updated"]) else 'Active'
            self.res["dataset_file_format"] = ["pdf", "xls", "zip"]
        except Exception as e:
            self.error_out(str(e), self.dataset_id)

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"
        return None
    
# ---------------------------------------------------
    # Old code for reference
# ---------------------------------------------------
# # Define a function to get the data attributes for an organization
# def get_data_attributes(url):

#     res = {i: "N/A" for i in ATTRS}
#     res['acronym'] = "RECS"
#     res["dataset_name"] = "Residential Energy Consumption Survey (RECS)"
#     res["dataset_website_link"] = ORG_URL

#     #Dataset Collection Method
#     DATASET_COLLECTION_METHOD = "The Household Survey, a voluntary survey, collects data on energy-related characteristics and usage patterns of a national and sub-national (e.g., states) representative sample of housing units. The Energy Supplier Survey (ESS), a mandatory data collection, collects data on how much electricity, natural gas, propane/LPG, and fuel oil/kerosene were consumed in the sampled housing units during the reference year. The ESS also collects data on actual dollar amounts spent on these energy sources. EIA uses models (energy engineering-based models in the 2015 and 2020 survey) to produce consumption and expenditures estimates for heating, cooling, refrigeration, and other end uses in all housing units occupied as a primary residence in the United States using the data collected from the Household Survey and ESS. Wood-use estimates are also included as part of RECS. The target population for the RECS is all occupied housing units in the 50 states and the District of Columbia (DC) that are used as primary residences. The 2020 RECS introduced a completely self-administered design via web and paper questionnaire."
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

#     #Sponsor Name
#     SPONSOR_NAME = "U.S. Energy Information Administration (EIA), a statistical agency of the U.S. Department of Energy."
#     res["sponsor_name"]=SPONSOR_NAME

#     #Citation Method
#     DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from https://www.eia.gov/consumption/residential/data/2020\n"
#     res["dataset_citation"] = DATASET_CITATION

#     #Type of access to the dataset
#     res["access_type"] = "Open Access"

#     about_info = "EIA administers the Residential Energy Consumption Survey (RECS) to a nationally representative sample of housing units. Traditionally, specially trained interviewers collect energy characteristics on the housing unit, usage patterns, and household demographics. For the 2020 survey cycle, EIA used Web and mail forms to collect detailed information on household energy characteristics. This information is combined with data from energy suppliers to these homes to estimate energy costs and usage for heating, cooling, appliances and other end uses — information critical to meeting future energy demand and improving efficiency and building design.\n\nFirst conducted in 1978, the fifteenth RECS collected data from nearly 18,500 households in housing units statistically selected to represent the 123.5 million housing units that are occupied as a primary residence. Data from the 2020 RECS are tabulated by geography and for particularly characteristics, such as housing unit type and income, that are of particular interest to energy analysis.\n\nThe results of each RECS include data tables, a microdata file, and a series of reports. Data tables are generally organized across two headings; 'Household Characteristics' and 'Consumption & Expenditures.'"
#     #Collect dataset info by redirecting to About this Survey page
#     res["about_info"] = about_info

#     response = requests.get(ORG_URL)
#     soup = BeautifulSoup(response.content,'html.parser')

#     #Get the dataset link
#     dataset_link = "https://www.eia.gov/" + soup.find('li', class_="dropdown").find('a').get('href')
#     res["dataset_link"] = dataset_link 

#     microdata = dataset_link + "/index.php?view=microdata"
#     response = requests.get(microdata)
#     soup = BeautifulSoup(response.content,'html.parser')
#     #Find when the dataset was last updated: DATA -> MICRODATA -> Release Date
#     last_updated = soup.find('table',class_='basic_table').find_all('td')[-1].get_text()
#     res["last_updated"]=last_updated
#     res['dataset_status'] = 'Inactive' if is_older_than_5yrs(res['last_updated']) else 'Active'
#     res["dataset_file_format"]=["pdf","xls","zip"]

#     return res