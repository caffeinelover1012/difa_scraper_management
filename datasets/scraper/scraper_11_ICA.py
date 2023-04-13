from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import date, datetime
from date_utils import *
from statics import *

DATE_FMT = "%d-%m-%Y"
ORG_URL = "https://www.cso.ie/en/methods/agricultureandfishing/censusofagriculture/"
ORGANIZATION = "ICA"

# Define a function to get the data attributes for an organization
def get_data_attributes():

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "Irish Census of Agriculture(ICA)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "Within the European Union (EU), each of the Member States will be tasked with collecting set data for the farmers and the farms above certain physical thresholds in their country. This will mean collecting data on as many as 10.5 million farms (2016 data) in the EU.\n\nMember States will establish teams of supervisors and enumerators to conduct the Agricultural Census, typically overseen by a combination of civil servants from the Statistical Office and the Ministry of Agriculture. They will use all types of collection methods to complete the Agricultural Census, inter alia farm registers, administrative sources and surveys. For the surveys, enumerators will contact farmers over the internet, by telephone, by letter or through face-to-face questioning. By allowing a more extensive use of administrative sources in 2020, the overall cost of the census will be reduced. At the same time, the burden on farmers will be alleviated, as they will receive questionnaires that are already partially pre-filled.\n\nIn the EU’s Agricultural Census 2020 approximately 300 variables will be collected, covering the following aspects on farming:\n\nGeneral characteristics of the farm and the farmer\nLand\nLivestock\nLabour force\nAnimal housing and manure management\nRural development support measures."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Irish Census of Agriculture dataset in APA format in your research paper, you can use the following citation format:\n\nCentral Statistics Office. (year of release). Census of Agriculture. [dataset]. Retrieved from [URL]\n\nFor example, in your reference list, the citation would look like this::\n\nCentral Statistics Office. (2016). Census of Agriculture 2010: Land Use, Output and Income - Detailed Tables. [dataset]. Retrieved from https://www.census.gov/programs-surveys/cps.html.\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "Central Statistics Office"
    res["sponsor_name"]=SPONSOR_NAME
    
    #Type of access to the dataset
    res["access_type"] = "Open Access"

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

    about_info = "An Agricultural Census is a statistical operation to compile census data on crops, livestock, farm labour and miscellaneous agricultural items for collecting, processing and disseminating data on all farms and farmers in a country.The Census of Agriculture survey is a statutory survey conducted every 10 years under the provisions of the Statistics (Census of Agriculture) Order, 2020 (S.I. No 281 of 2020). Under Sections 26 and 27 of the 1993 Statistics Act you are obliged by law to complete and return this form. Any person who fails or refuses to provide this information or who knowingly provides false information may be subject to prosecution under Part VI of the Act."
    #Collect dataset info by redirecting to About this Survey page
    res["about_info"] = about_info

    #Find when the dataset was last updated
    last_updated=browser.find_element(By.XPATH,'//*[@id="dateModified"]/p').text
    last_updated_date=standardize(DATE_FMT,last_updated[19:])
    res["last_updated"]=last_updated_date

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=last_updated_date[-4:]
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    browser.find_element(By.XPATH,'//*[@id="110099li_12"]/a').click()
    sleep(3)
    dataset_link = browser.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div/div[2]/div/div[2]/ul/li[1]/a').get_attribute('href')
    res["dataset_link"] = dataset_link 

    res["dataset_file_format"]=["pdf"]

    #Close and quit all browser driver instances
    browser.quit()

    return res

# result=get_data_attributes()
# print(result)
