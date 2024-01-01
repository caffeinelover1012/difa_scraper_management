from .BaseScraper import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.safegraph.com/"
ORGANIZATION = "SafeGraph"
ABOUT = """SafeGraph is a data company that collects and provides datasets related to location-based analytics. The SafeGraph dataset contains anonymized data on foot traffic patterns at various locations, such as businesses, points of interest, and residential areas. The dataset includes information on the number of visitors to these locations, the duration of their visits, and other relevant data points. SafeGraph is narrowly focused on building the most accurate global places dataset available, empowering modern builders to create world-class location-based applications and analytics tools. SafeGraph curates the most accurate and precise database of global points of interest each month to power applications, platforms, and services with a location component. As a source of truth for the physical world, SafeGraph data provides an up-to-date record of where places are located and detailed attribution about each of those places, such as when it opened or closed, what type of place it is, what other places it is affiliated with, and how people interact with that location. SafeGraph delivers high quality data in a unified schema to reduce time spent cleaning and munging data, and serves as a partner in data curation and sourcing for organizations building location-based products and services. Keep reading our technical docs to see our schema, monthly metrics, and helpful information about data delivery and evaluations."""
DATASET_COLLECTION_METHOD = "Safegraph dataset is collected through mobile devices such as smartphones. The company collects location data from apps installed on mobile devices that opt-in to location tracking. The data is collected and aggregated into anonymized patterns and then made available to researchers and businesses for analysis. The Safegraph dataset includes various types of location data, including visitation patterns to specific places, foot traffic, and demographic information. The dataset is updated regularly to provide up-to-date information on location trends and changes."
DATASET_NAME = "SafeGraph"
SPONSOR_NAME = "SafeGraph"

class SafeGraph(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': DATASET_NAME,
            'access_type': self.constants['PAID_ACCESS'],
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_website_link': ORG_URL,
            'dataset_link': "https://docs.safegraph.com/docs/bulk-data-delivery",
            'dataset_file_format': ["CSV", "JSON", "Parquet"],
            'dataset_collection_method': DATASET_COLLECTION_METHOD,
            'about_info': ABOUT,
            'other_info':"https://docs.safegraph.com/docs/faqs"
            })

        date_url = "https://docs.safegraph.com/docs/open-census-data"
        date_soup = self.fetch_data_with_requests(date_url)
        self.extract_data_attributes(date_soup=date_soup)
        self.finalize_additional_attributes()

    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)
        date_soup = kwargs.get('date_soup')
        
        try:
            updateText = date_soup.find('div', attrs={'class': 'UpdatedAt'}).getText()
            last_update = is_older_than_5_yrs_str(updateText)
            self.res['dataset_status'] = 'Inactive' if last_update else 'Active'
        except Exception as e:
            self.error_out(str(e), self.dataset_id)

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"
        return None

# ---------------------------------------------------
    # Old code for reference
# ---------------------------------------------------
# def get_data_attributes(url):
    
#     res = {i: "N/A" for i in ATTRS}
#     res['acronym'] = "SafeGraph"
#     res['dataset_website_link'] = ORG_URL
#     res['access_type'] = 'Paid Access'
#     res['last_updated'] = "Monthly"
#     res['sponsor_name'] = "SafeGraph"
#     res['dataset_name'] = "SafeGraph"
#     res['dataset_link'] = "https://docs.safegraph.com/docs/bulk-data-delivery"
#     res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from {res['dataset_link']}\n"
#     # Make a request to the organization's website
#     response = requests.get("https://docs.safegraph.com/docs/open-census-data")
#     # Parse the HTML content of the response using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#     updateText = soup.find('div', attrs={'id': 'updated-at'}).getText()
#     last_update = is_older_than_5_yrs_str(updateText)
#     if last_update == True:
#         res['dataset_status'] = 'Inactive'
#     else:
#         res['dataset_status'] = 'Active'
#     res['about_info'] = about
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD
#     formats = {'CSV': None, 'JSON': None, 'Parquet': None}
#     res['dataset_file_format'] = list(formats.keys())
#     res['other_info'] = "https://docs.safegraph.com/docs/faqs"
#     return res
