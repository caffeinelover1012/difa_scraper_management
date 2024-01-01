from .BaseScraper import *

DATE_FMT = "%d %B %Y"
ORG_URL = "https://prism.oregonstate.edu/"
ORGANIZATION = "PRISM"
DATASET_NAME = "PRISM"
DATASET_COLLECTION_METHOD = "The PRISM dataset is collected through a process called parameter-elevation regressions on independent slopes model (PRISM). PRISM is a statistically-based, spatially-distributed climate model that uses a variety of input data sources to produce high-resolution climate data estimates for specific locations and time periods.\n\nThe input data for PRISM includes weather station data, remote sensing data, and digital elevation models. These data are combined using statistical models to create climate data estimates for various climate variables, such as temperature and precipitation, at high spatial resolutions.\n\nPRISM is designed to account for topographic and climatic differences across different regions, and is continuously updated as new data becomes available. The resulting PRISM dataset is widely used by researchers, government agencies, and other stakeholders for a variety of applications, including climate monitoring, water resource management, agriculture, and ecological modeling."
SPONSOR_NAME = "The PRISM Climate Group (Oregon State University)"
ABOUT_INFO = "The PRISM Climate Group gathers climate observations from a wide range of monitoring networks, applies sophisticated quality control measures, and develops spatial climate datasets to reveal short- and long-term climate patterns. The resulting datasets incorporate a variety of modeling techniques and are available at multiple spatial/temporal resolutions, covering the period from 1895 to the present. PRISM datasets provide estimates of seven primary climate elements: precipitation (ppt), minimum temperature (tmin), maximum temperature (tmax), mean dew point (tdmean), minimum vapor pressure deficit (vpdmin), maximum vapor pressure deficit (vpdmax), and total global shortwave solar radiation on a horizontal surface (soltotal; available only as normals at this time). Mean temperature (tmean) is derived as the average of tmax and tmin. Three ancillary solar radiation variables are provided in the normals dataset: total global solar radiation on a horizontal surface under clear sky conditions (solclear), effective cloud transmittance (soltrans), and total global solar radiation on a sloped surface (solslope)."


class PRISM(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "PRISM",
            'dataset_website_link': ORG_URL,
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_collection_method': DATASET_COLLECTION_METHOD,
            'about_info': ABOUT_INFO,
            'dataset_file_format': ["png", "zip", "bil", "xml", "hdr", "txt", "csv", "prj", "stx"],
            # Dataset link and other details will be set after fetching the actual data
        })
        self.main_page_soup = self.fetch_data_with_requests(ORG_URL)
        self.extract_data_attributes(main_page_soup=self.main_page_soup)
        self.finalize_additional_attributes()

    
    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)
        main_page_soup = kwargs.get('main_page_soup')

        try:
            dataset_links = [{"30-Year Normals":"https://prism.oregonstate.edu/normals","Comparisons":"https://prism.oregonstate.edu/comparisons",
                      "This Month":"https://prism.oregonstate.edu/mtd","Prior 6 Months":"https://prism.oregonstate.edu/6month/",
                      "Recent Years":"https://prism.oregonstate.edu/recent","Historical Past":"https://prism.oregonstate.edu/historical",
                      "Projects":"https://prism.oregonstate.edu/projects","Data Explorer":"https://prism.oregonstate.edu/explorer"}]
            self.res["dataset_link"] = dataset_links

            # Check dataset status from the footer of the webpage
            footer = main_page_soup.find('div', id="footer").get_text()
            current_year = date.today().year

            if str(current_year) in footer:
                self.res["dataset_status"] = "Active"
                self.res["last_updated"] = date.today().strftime('%B %d, %Y')
            else:
                self.res["dataset_status"] = "Inactive"
                # If inactive, last updated date might require a different approach

        except Exception as e:
            self.error_out(str(e), self.dataset_id)

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"
        return None
# # Define a function to get the data attributes for an organization
# def get_data_attributes(url):

#     res = {i: "N/A" for i in ATTRS}
#     res['acronym'] = "PRISM"
#     res["dataset_name"] = "PRISM"
#     res["dataset_website_link"] = ORG_URL

#     #Dataset Collection Method
#     DATASET_COLLECTION_METHOD = "The PRISM dataset is collected through a process called parameter-elevation regressions on independent slopes model (PRISM). PRISM is a statistically-based, spatially-distributed climate model that uses a variety of input data sources to produce high-resolution climate data estimates for specific locations and time periods.\n\nThe input data for PRISM includes weather station data, remote sensing data, and digital elevation models. These data are combined using statistical models to create climate data estimates for various climate variables, such as temperature and precipitation, at high spatial resolutions.\n\nPRISM is designed to account for topographic and climatic differences across different regions, and is continuously updated as new data becomes available. The resulting PRISM dataset is widely used by researchers, government agencies, and other stakeholders for a variety of applications, including climate monitoring, water resource management, agriculture, and ecological modeling."
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD
    
#     #Sponsor Name
#     SPONSOR_NAME = "The PRISM Climate Group, Oregon State University."
#     res["sponsor_name"] = SPONSOR_NAME

#     #Citation Method
#     DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from https://prism.oregonstate.edu/normals\n"
#     res["dataset_citation"] = DATASET_CITATION

#     #Type of access to the dataset
#     res["access_type"] = "Open Access" #Fee applied depending on dataset size/complexity and funding available for the activity.

#     ABOUT_INFO = "The PRISM Climate Group gathers climate observations from a wide range of monitoring networks, applies sophisticated quality control measures, and develops spatial climate datasets to reveal short- and long-term climate patterns. The resulting datasets incorporate a variety of modeling techniques and are available at multiple spatial/temporal resolutions, covering the period from 1895 to the present. PRISM datasets provide estimates of seven primary climate elements: precipitation (ppt), minimum temperature (tmin), maximum temperature (tmax), mean dew point (tdmean), minimum vapor pressure deficit (vpdmin), maximum vapor pressure deficit (vpdmax), and total global shortwave solar radiation on a horizontal surface (soltotal; available only as normals at this time). Mean temperature (tmean) is derived as the average of tmax and tmin. Three ancillary solar radiation variables are provided in the normals dataset: total global solar radiation on a horizontal surface under clear sky conditions (solclear), effective cloud transmittance (soltrans), and total global solar radiation on a sloped surface (solslope)."
#     res["about_info"] = ABOUT_INFO

#     #Get the dataset link
#     dataset_links = [{"30-Year Normals":"https://prism.oregonstate.edu/normals","Comparisons":"https://prism.oregonstate.edu/comparisons",
#                       "This Month":"https://prism.oregonstate.edu/mtd","Prior 6 Months":"https://prism.oregonstate.edu/6month/",
#                       "Recent Years":"https://prism.oregonstate.edu/recent","Historical Past":"https://prism.oregonstate.edu/historical",
#                       "Projects":"https://prism.oregonstate.edu/projects","Data Explorer":"https://prism.oregonstate.edu/explorer"}]
#     res["dataset_link"] = dataset_links

#     response = requests.get('https://prism.oregonstate.edu/')
#     soup = BeautifulSoup(response.content,'html.parser')

#     #Find the status of the dataset by checking the footer of webpage.
#     footer = soup.find('div',id="footer").get_text()
#     current_date=date.today()
#     current_year=current_date.year

#     status="Inactive"
#     if str(current_year) in footer:
#         status="Active"
#         #Find when the dataset was last updated
#         last_updated_date = current_date.strftime('%B %d, %Y')
#         res["last_updated"]=last_updated_date
        
#     res["dataset_status"]=status

#     res["dataset_file_format"]=["png","zip","bil","xml","hdr","txt","csv","prj","stx"]

#     return res