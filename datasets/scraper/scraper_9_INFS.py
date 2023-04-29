from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import date, datetime
from .common_imports import *
DATE_FMT = "%d %B %Y"
ORG_URL = "https://www.teagasc.ie/rural-economy/rural-economy/national-farm-survey/"
ORGANIZATION = "NFS"
DATASET_NAME = "Irish National Farm Survey (NFS)"

def get_data_attributes(url):
    res = {i: "N/A" for i in ATTRS}

    #Create a dictionary to store dataset info
    res["dataset_name"] = "Irish National Farm Survey (NFS)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The data collected cover all the key financial and physical indicators at farm level viz inventories, sales, purchases, costs, subsidies, liabilities, assets, cropping programme, yields etc.\n\nIn recent years the NFS has extended the range of data covered to the farm household, as the increased emphasis on rural development and viability of rural communities has placed greater emphasis on farm household data e.g. off-farm employment and income, farm inheritance, household composition, age structure etc. Additional data are also being collected regarding environmental issues.\n\nData is collected using laptop computers on a regular basis throughout the year by a team of trained Teagasc Research Technicians located throughout the country. The NFS has always been conducted to ensure total confidentiality of individual farmer’s data. A unique code is used to identify each farm thus ensuring that data cannot be linked to a particular farm."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Irish National Farm Survey (NFS) dataset in APA format in your research paper, you can use the following citation format:\n\nTeagasc. (year of release). National Farm Survey [Data set]. Retrieved from [URL]\n\nFor example, in your reference list, the citation would look like this:\n\nTeagasc. (2020). National Farm Survey 2019 [Data set]. Retrieved from https://www.teagasc.ie/publications/surveys/national-farm-survey/national-farm-survey-2019.php\n\nMake sure to replace the [year of release] with the year your dataset was released, the [Data set] with name of your dataset used, and the [URL] with the specific URL of the dataset you used."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "Teagasc, the Irish Agriculture and Food Development Authority."
    res["sponsor_name"] = SPONSOR_NAME

    #Type of access to the dataset
    res["access_type"] = "Open Access"
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url)
    sleep(3)
    #Accept cookies on the page
    browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[1]/div/div[2]/div/button[3]').click()
    about_info = ""
    #Collect dataset info from main page
    about1 = browser.find_element(By.XPATH,'/html/body/main/div/article/p[1]').text
    about2 = browser.find_element(By.XPATH,'/html/body/main/div/article/p[2]').text
    about_info = about1 + "\n\n" + about2

    #Store About info to dictionary
    res["about_info"] = about_info

    #Find the main uses of Irish NFS dataset
    dataset_usage = []
    uses = browser.find_elements(By.XPATH ,'/html/body/main/div/article/p[*]/strong')
    for use in uses:
        dataset_usage.append(use.text)
    res["other_info"] = [{"dataset_usage":dataset_usage}]

    # Get the INFS dataset link
    DATASET_LINK = "https://www.ucd.ie/issda/data/"
    DATASET_REPORTS = "https://www.teagasc.ie/rural-economy/rural-economy/national-farm-survey/national-farm-survey-reports/"
    ISSDA_DATA_REQUEST_FORM = "https://www.ucd.ie/issda/t4media/ISSDA_Application_Research_V5.docx"
    INFS_DATA_ACCESS_INFO = "To access the data, please complete a ISSDA Data Request Form for Research Purposes\n\nLink to download form:" + ISSDA_DATA_REQUEST_FORM + "\n\nsign it, and send it to ISSDA by email <issda@ucd.ie>.\n\nData will be disseminated on receipt of a fully completed, signed form. Incomplete or unsigned forms will be returned to the data requester for completion."

    res["dataset_link"]=DATASET_LINK
    res["dataset_file_format"]=["pdf"]
    res["other_info"].append({"dataset_access_info":INFS_DATA_ACCESS_INFO})
    res["other_info"].append({"dataset_reports":DATASET_REPORTS})

    #Click on National Farm Survey Reports tab
    browser.find_element(By.XPATH, '/html/body/main/div/div[1]/div/nav/ul/li[1]/ul/li[1]/a').click()

    #Go to the latest collected report page
    browser.find_element(By.XPATH, '/html/body/main/div/article/ul/li[1]/a').click()

    # Find the last updated date of data and compute if the last collected is not more than 5 years of duration.
    last_updated = browser.find_element(By.XPATH,'/html/body/main/div/article/div/article/div/div').text.split('\n')[0]
    last_updated_date = standardize(DATE_FMT,last_updated)
    res["last_updated"] = last_updated_date

    latest_year_available = int(last_updated.strip()[-4:])
    current_date = date.today()
    current_year = current_date.year
    year_difference = int(current_year)-int(latest_year_available)
    status = "Active"
    if year_difference >= 5:
        status = "Inactive"
    res["dataset_status"] = status

    #Close and quit all browser driver instances
    browser.quit()

    return res



# # Loop through the organization dictionary and print the data attribute output
# print(ORGANIZATION)
# print('-' * len(ORGANIZATION))
# data_attributes = get_data_attributes(ORG_URL)
# for attribute, value in data_attributes.items():
#     print(f'{attribute}: {value}', end="\n\n")
# print()