from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import date, datetime
from date_utils import *
from statics import *

DATE_FMT = "%d %B %Y"
ORG_URL = "https://prism.oregonstate.edu/"
ORGANIZATION = "PRISM"

# Define a function to get the data attributes for an organization
def get_data_attributes():

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "PRISM"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The PRISM dataset is collected through a process called parameter-elevation regressions on independent slopes model (PRISM). PRISM is a statistically-based, spatially-distributed climate model that uses a variety of input data sources to produce high-resolution climate data estimates for specific locations and time periods.\n\nThe input data for PRISM includes weather station data, remote sensing data, and digital elevation models. These data are combined using statistical models to create climate data estimates for various climate variables, such as temperature and precipitation, at high spatial resolutions.\n\nPRISM is designed to account for topographic and climatic differences across different regions, and is continuously updated as new data becomes available. The resulting PRISM dataset is widely used by researchers, government agencies, and other stakeholders for a variety of applications, including climate monitoring, water resource management, agriculture, and ecological modeling."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the PRISM dataset in APA format in your research paper, you can use the following citation format:\n\nPRISM Climate Group. (Year). PRISM Climate Data [Data set]. Oregon State University. Retrieved from [URL] \n\nFor example, in your reference list, the citation would look like this::\n\nPRISM Climate Group. (2021). PRISM Climate Data [Data set]. Oregon State University. Retrieved from https://prism.oregonstate.edu/\n\nWhen the data are used, any description should clearly and prominently state, at a minimum, sponsor name, URL, and the dates of data creation and access. For example:\nPRISM Climate Group, Oregon State University, https://prism.oregonstate.edu, data created 4 Feb 2014, accessed 16 Dec 2020.\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "The PRISM Climate Group, Oregon State University."
    res["sponsor_name"] = SPONSOR_NAME

    #Type of access to the dataset
    res["access_type"] = "Open Access" #Fee applied depending on dataset size/complexity and funding available for the activity.

    ABOUT_INFO = "The PRISM Climate Group gathers climate observations from a wide range of monitoring networks, applies sophisticated quality control measures, and develops spatial climate datasets to reveal short- and long-term climate patterns. The resulting datasets incorporate a variety of modeling techniques and are available at multiple spatial/temporal resolutions, covering the period from 1895 to the present. PRISM datasets provide estimates of seven primary climate elements: precipitation (ppt), minimum temperature (tmin), maximum temperature (tmax), mean dew point (tdmean), minimum vapor pressure deficit (vpdmin), maximum vapor pressure deficit (vpdmax), and total global shortwave solar radiation on a horizontal surface (soltotal; available only as normals at this time). Mean temperature (tmean) is derived as the average of tmax and tmin. Three ancillary solar radiation variables are provided in the normals dataset: total global solar radiation on a horizontal surface under clear sky conditions (solclear), effective cloud transmittance (soltrans), and total global solar radiation on a sloped surface (solslope)."
    res["about_info"] = ABOUT_INFO

    #Initialize Browser
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    # To maximize the browser window
    browser.maximize_window()
    browser.get(ORG_URL)
    sleep(3)

    #Get the dataset link
    dataset_links = []
    links = browser.find_elements(By.XPATH,'//*[@id="wrapper"]/p[*]/a')
    for link in links:
        dataset_links.append(link.get_attribute('href'))
    res["dataset_link"] = dataset_links

    #Find the status of the dataset by checking the footer of webpage.
    footer = browser.find_element(By.XPATH,'//*[@id="footer"]').text
    current_date=date.today()
    current_year=current_date.year

    status="Inactive"
    if str(current_year) in footer:
        status="Active"
        #Find when the dataset was last updated
        last_updated_date = current_date.strftime('%B %d, %Y')
        res["last_updated"]=last_updated_date

    res["dataset_status"]=status

    res["dataset_file_format"]=["png","zip","bil","xml","hdr","txt","csv","prj","stx"]

    #Close and quit all browser driver instances
    browser.quit()

    return res

# result=get_data_attributes()
# print(result)
