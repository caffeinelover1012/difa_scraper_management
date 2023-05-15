from .common_imports import *

DATE_FMT = "%B %d, %Y"
ORG_URL = "https://www.census.gov/programs-surveys/cps.html"
ORGANIZATION = "CPS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "Current Population Survey (CPS)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The CPS is administered by the Census Bureau using a probability selected sample of about 60,000 occupied households. The fieldwork is conducted during the calendar week that includes the 19th of the month. The questions refer to activities during the prior week; that is, the week that includes the 12th of the month. Households from all 50 states and the District of Columbia are in the survey for 4 consecutive months, out for 8, and then return for another 4 months before leaving the sample permanently. This design ensures a high degree of continuity from one month to the next (as well as over the year). The 4-8-4 sampling scheme has the added benefit of allowing the constant replenishment of the sample without excessive burden to respondents.\n\nThe CPS questionnaire is a completely computerized document that is administered by Census Bureau field representatives across the country through both personal and telephone interviews. Additional telephone interviewing is conducted from the Census Bureau’s two centralized collection facilities in Jeffersonville, Indiana and Tucson, Arizona.\n\nMore information can be found at: https://www.census.gov/programs-surveys/cps/technical-documentation/methodology.html"
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Sponsor Name
    SPONSOR_NAME = "US Census Bureau"
    res["sponsor_name"]=SPONSOR_NAME

    GENERAL_DATASET_SEARCH_TOOL_MDAT = "https://data.census.gov/mdat/#/"
    res["dataset_link"] = GENERAL_DATASET_SEARCH_TOOL_MDAT

    #Citation Method
    DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from {res['dataset_link']}\n"
    res["dataset_citation"] = DATASET_CITATION

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

    about_info = ""
    #Collect dataset info by redirecting to About this Survey page
    browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[6]/div/div[2]/nav/ul/li[1]/a').click()
    # sleep(3)
    paragraphs = browser.find_elements(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[1]/div/section/div/*')
    for para in paragraphs:
        about_info += para.text
    res["about_info"] = about_info

    #Go back to the main page.
    browser.find_element(By.XPATH,'//*[@id="breadContainer"]/ul/li[3]/a').click()
    # sleep(3)

    #Get the CPS datasets
    browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[6]/div/div[2]/nav/ul/li[2]/a').click()
    sleep(3)
    browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[8]/div/div/div/div[1]/div[2]/a[3]').click()
    sleep(3)
    cps_datasets = []
    all_datasets = browser.find_elements(By.XPATH,'//*[@id="listArticlesContainer_List_925177770"]/div[2]/a[*]')
    basic_cps = ""
    i=0
    for dataset in all_datasets:
        if i == 1:
            basic_cps = dataset
        cps_datasets.append((dataset.text,dataset.get_attribute('href')))
        i+=1

    res["other_info"] = cps_datasets 

    res["dataset_file_format"]=["csv","pdf","sas","txt"]

    #Click on data release plan to see the latest data
    basic_cps.click()
    # sleep(3)

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div/ul/li[1]/a').text
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    #Find when the dataset was last updated
    last_updated=browser.find_element(By.XPATH,'//*[@id="uscb-automation-lastmodified-date"]').text
    last_updated_date=standardize(DATE_FMT,last_updated[20:])
    res["last_updated"]=last_updated_date

    #Close and quit all browser driver instances
    browser.quit()

    return res
