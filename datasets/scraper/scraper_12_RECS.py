import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date, datetime
from date_utils import *
from statics import *

DATE_FMT = "%d %B %Y"
ORG_URL = "https://www.eia.gov/consumption/residential/"
ORGANIZATION = "RECS"

# Define a function to get the data attributes for an organization
def get_data_attributes():

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "Residential Energy Consumption Survey (RECS)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The Household Survey, a voluntary survey, collects data on energy-related characteristics and usage patterns of a national and sub-national (e.g., states) representative sample of housing units. The Energy Supplier Survey (ESS), a mandatory data collection, collects data on how much electricity, natural gas, propane/LPG, and fuel oil/kerosene were consumed in the sampled housing units during the reference year. The ESS also collects data on actual dollar amounts spent on these energy sources. EIA uses models (energy engineering-based models in the 2015 and 2020 survey) to produce consumption and expenditures estimates for heating, cooling, refrigeration, and other end uses in all housing units occupied as a primary residence in the United States using the data collected from the Household Survey and ESS. Wood-use estimates are also included as part of RECS. The target population for the RECS is all occupied housing units in the 50 states and the District of Columbia (DC) that are used as primary residences. The 2020 RECS introduced a completely self-administered design via web and paper questionnaire."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Residential Energy Consumption Survey dataset in APA format in your research paper, you can use the following citation format:\n\nU.S. Energy Information Administration. (year). Residential Energy Consumption Survey (RECS) [Data set]. Retrieved from [URL]\n\nFor example, in your reference list, the citation would look like this::\n\nU.S. Energy Information Administration. (2021). Residential Energy Consumption Survey (RECS) [Data set]. Retrieved from https://www.eia.gov/consumption/residential/data/2021/\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "U.S. Energy Information Administration (EIA), a statistical agency of the U.S. Department of Energy."
    res["sponsor_name"]=SPONSOR_NAME
    
    #Type of access to the dataset
    res["access_type"] = "Open Access"

    #Initialize Browser
    browser = webdriver.Chrome()
    # To maximize the browser window
    browser.maximize_window()
    browser.get(ORG_URL)
    sleep(3)

    about_info = "EIA administers the Residential Energy Consumption Survey (RECS) to a nationally representative sample of housing units. Traditionally, specially trained interviewers collect energy characteristics on the housing unit, usage patterns, and household demographics. For the 2020 survey cycle, EIA used Web and mail forms to collect detailed information on household energy characteristics. This information is combined with data from energy suppliers to these homes to estimate energy costs and usage for heating, cooling, appliances and other end uses — information critical to meeting future energy demand and improving efficiency and building design.\n\nFirst conducted in 1978, the fifteenth RECS collected data from nearly 18,500 households in housing units statistically selected to represent the 123.5 million housing units that are occupied as a primary residence. Data from the 2020 RECS are tabulated by geography and for particularly characteristics, such as housing unit type and income, that are of particular interest to energy analysis.\n\nThe results of each RECS include data tables, a microdata file, and a series of reports. Data tables are generally organized across two headings; 'Household Characteristics' and 'Consumption & Expenditures.'"
    #Collect dataset info by redirecting to About this Survey page
    res["about_info"] = about_info

    #Get the dataset link
    dataset_link = browser.find_element(By.XPATH,'//*[@id="innerX"]/div[2]/ul/li[2]/a').get_attribute('href')
    res["dataset_link"] = dataset_link 
    browser.find_element(By.XPATH,'//*[@id="innerX"]/div[2]/ul/li[2]/a').click()
    sleep(3)
    browser.find_element(By.XPATH,'//*[@id="tab-container"]/ul/a[2]').click()
    sleep(3)

    #Find when the dataset was last updated: DATA -> MICRODATA -> Release Date
    last_updated = browser.find_element(By.XPATH,'//*[@id="microdata"]/table/tbody/tr/td[4]').text
    print(last_updated)
    res["last_updated"]=last_updated

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=last_updated[-4:]
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    res["dataset_file_format"]=["pdf","xls","zip"]

    #Close and quit all browser driver instances
    browser.quit()

    return res

# result=get_data_attributes()
# print(result)
