from .BaseScraper import *

DATE_FMT = "%B %d, %Y"
ORG_URL = "https://www.census.gov/programs-surveys/acs"
ORGANIZATION = "ACS"
SPONSOR_NAME = "US Census Bureau"
DATASET_NAME = "American Community Survey (ACS)"
DATASET_COLLECTION_METHOD = "The American Community Survey (ACS) is an ongoing survey conducted by the US Census Bureau. The survey collects data on a range of social, economic, and housing characteristics of the US population on a continuous basis throughout the year. The ACS is conducted using both mail and in-person interviews, and respondents are selected through a random sampling process. The survey is designed to be representative of the entire US population, including people living in households and group quarters (such as college dormitories, correctional facilities, and nursing homes). The data collected through the ACS is used by a wide range of organizations, including government agencies, academic researchers, and non-profit organizations, to better understand the needs of US communities and make informed decisions."

about_info = ""
#Collect dataset info from main page
overview_text = "The American Community Survey (ACS) helps local officials, community leaders, and businesses understand the changes taking place in their communities. It is the premier source for detailed population and housing information about our nation."
about_info += overview_text
about1 = " The American Community Survey (ACS) is an ongoing survey that provides vital information on a yearly basis about our nation and its people. Information from the survey generates data that help determine how more than $675 billion in federal and state funds are distributed each year."
about2 = " Through the ACS, we know more about jobs and occupations, educational attainment, veterans, whether people own or rent their homes, and other topics. Public officials, planners, and entrepreneurs use this information to assess the past and plan the future. When you respond to the ACS, you are doing your part to help your community plan for hospitals and schools, support school lunch programs, improve emergency services, build bridges, and inform businesses looking to add jobs and expand to new markets, and more."
about_info = about_info + "\n\n" + about1 + "\n\n" + about2
ABOUT = about_info



class ACS(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "ACS",
            'access_type': self.constants['OPEN_ACCESS'],
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_website_link': ORG_URL,
            'dataset_link': "https://data.census.gov/",
            'dataset_collection_method': DATASET_COLLECTION_METHOD,
            'dataset_file_format': ["csv", "excel"],
            'about_info': ABOUT,
        })
        
        self.extract_data_attributes()
        self.finalize_additional_attributes()

    def find_latest_data_release_year(self):
        base_url = "https://www.census.gov/programs-surveys/acs/news/data-releases/"
        current_year = datetime.now().year
        for year in range(current_year, current_year - 10, -1):
            url = f"{base_url}{year}/release.html"
            response = requests.get(url)
            if response.status_code == 200:
                return year
        return None

    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)

        try:
            latest_year = self.find_latest_data_release_year()
            if latest_year:
                latest_data_url = f"https://www.census.gov/programs-surveys/acs/news/data-releases/{latest_year}/release.html"
                latest_data_soup = self.fetch_data_with_requests(latest_data_url)
                
                date_elements = latest_data_soup.find_all('div', class_='cmp-title')
                for element in date_elements:
                    h5_element = element.find('h5')
                    if h5_element:
                        date_text = h5_element.get_text()
                        try:
                            parsed_date = datetime.strptime(date_text, DATE_FMT)
                            self.res["last_updated"] = parsed_date.strftime(DATE_FMT)
                            break
                        except ValueError:
                            continue

                year_difference = datetime.now().year - latest_year
                self.res["dataset_status"] = 'Inactive' if year_difference >= 5 else 'Active'
            else:
                self.res["last_updated"] = "N/A"
                self.res["dataset_status"] = "N/A"

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
#     res['acronym'] = "ACS"
#     res["dataset_name"] = 
#     res["dataset_website_link"] = ORG_URL
    
#     #Dataset Collection Method
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD
    
#     #Sponsor Name
#     res["sponsor_name"]=SPONSOR_NAME
    
#     res["dataset_citation"] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from https://data.census.gov/\n"
    
#     res["access_type"] = OPEN_ACCESS


    #Store About info to dictionary
    # res["about_info"] = about_info

#     #Get the ACS data link from Data -> data.census.gov - https://data.census.gov/
#     acs_dataset_link="https://data.census.gov/"
#     res["dataset_link"]=acs_dataset_link
#     res["dataset_file_format"]=["csv","excel"]

#     #Click on data release plan to see the latest data
#     response = requests.get("https://www.census.gov/programs-surveys/acs/news/data-releases.html")
#     soup = BeautifulSoup(response.content,'html.parser')


#     #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
#     latest_year_available = soup.find('a',class_='uscb-tabs-link uscb-padding-LR-10').get_text()
    
#     current_date=date.today()
#     current_year=current_date.year
#     year_difference=int(current_year)-int(latest_year_available)
#     status="Active"
#     if year_difference>=5:
#         status="Inactive"
#     res["dataset_status"]=status

#     latest_link = "https://www.census.gov/" + soup.find('div',id='listArticlesContainer_List_1929147522').find('a').get('href')
    
#     #Find when the dataset was last updated
#     response = requests.get(latest_link)
#     soup = BeautifulSoup(response.content,'html.parser')
    
#     last_updated = soup.find('div',id='textcore-43ff463df2').find('i').get_text()
#     last_updated_date=standardize(DATE_FMT,last_updated[8:])
#     res["last_updated"]=last_updated_date
    
#     return res