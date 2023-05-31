from .common_imports import *

DATE_FMT = "%B %d, %Y"
ORG_URL = "https://www.census.gov/programs-surveys/acs"
ORGANIZATION = "ACS"

# Define a function to get the data attributes for an organization
def get_data_attributes():

    res = {i: "N/A" for i in ATTRS}
    res["dataset_name"] = "American Community Survey (ACS)"
    res["dataset_website_link"] = ORG_URL
    
    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The American Community Survey (ACS) is an ongoing survey conducted by the US Census Bureau. The survey collects data on a range of social, economic, and housing characteristics of the US population on a continuous basis throughout the year. The ACS is conducted using both mail and in-person interviews, and respondents are selected through a random sampling process. The survey is designed to be representative of the entire US population, including people living in households and group quarters (such as college dormitories, correctional facilities, and nursing homes). The data collected through the ACS is used by a wide range of organizations, including government agencies, academic researchers, and non-profit organizations, to better understand the needs of US communities and make informed decisions."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD
    
    #Sponsor Name
    SPONSOR_NAME = "US Census Bureau"
    res["sponsor_name"]=SPONSOR_NAME
    
    res["dataset_citation"] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from https://data.census.gov/\n"
    
    res["access_type"] = OPEN_ACCESS

    # Initialize Browser
    options = Options()
    options.add_argument("--disable-features=Permissions-Policy")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    # To maximize the browser window
    browser.maximize_window()
    browser.get(ORG_URL)
    sleep(3)

    about_info = ""
    #Collect dataset info from main page
    overview_text = browser.find_element(By.XPATH,'//*[@id="textcore-e064157133"]/p').text
    about_info += overview_text

    #Redirect to about the ACS page and gather about info
    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[6]/div/div[2]/nav/ul/li[1]/a").click()
    sleep(3)
    about1 = browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[1]/div/section/div[2]/p[2]').text
    about2 = browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[2]/div/section/div[2]/p[2]').text
    about_info = about_info + "\n\n" + about1 + "\n\n" + about2
    #Store About info to dictionary
    res["about_info"] = about_info

    #Go back to the main page.
    browser.find_element(By.XPATH,'//*[@id="breadContainer"]/ul/li[3]/a').click()
    sleep(3)

    #Get the ACS data link from Data -> data.census.gov - https://data.census.gov/
    acs_dataset_link=browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[8]/div/div[4]/div/div/div[2]/div/a[2]").get_attribute('href')
    res["dataset_link"]=acs_dataset_link
    res["dataset_file_format"]=["csv","excel"]

    #Click on data release plan to see the latest data
    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[8]/div/div[4]/div/div/div[2]/div/a[1]").click()
    sleep(3)

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[2]/ul/li[1]/a').text
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    #Find when the dataset was last updated
    browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/a[1]').click()
    sleep(3)
    last_updated=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div[10]/div/div[1]/div').text
    last_updated_date=standardize(DATE_FMT,last_updated[8:])
    res["last_updated"]=last_updated_date

    return res