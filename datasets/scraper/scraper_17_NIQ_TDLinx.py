from .common_imports import *


DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://nielseniq.com/global/en/solutions/tdlinx/"
ORGANIZATION = "NIQ TDLinx"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "NIQ TDLinx"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The Nielsen TDLinx dataset is collected through field visits and data collection processes that involve scanning and recording information about retail stores. The data includes information about store locations, attributes such as size and type of store, and the products sold in those stores. The information is collected by trained field staff who visit the stores and gather data using specialized equipment and software. The data is then processed and compiled into the TDLinx dataset for use by researchers, businesses, and other interested parties."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Nielsen TDLinx dataset in APA format in your research paper, you can use the following citation format:\n\nNielsen (Year). TDLinx [Dataset]. NielsenIQ. Retrieved from [URL]. \n\nFor example, in your reference list, the citation would look like this::\n\nNielsen. (2021). Nielsen TDLinx [Dataset]. Retrieved from https://www.nielsen.com/us/en/solutions/capabilities/retail-measurement/tdlinx/\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "NielsenIQ"
    res["sponsor_name"] = SPONSOR_NAME

    #Type of access to the dataset
    res["access_type"] = "Restriced and Paid Access"

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

    about_info = "Nielsen TDLinx dataset is a dynamic catalog of retail and on-premise location information that delivers a consistent view of store-level performance and startegic needs. NIQ TDLinx provides location-based and store-level insights to make data-driven distribution decisions with ease. Using this dataset one can monitor the retail footprint and pinpoint opportunities to expand brand’s reach in key retail and on-premise channels."
    res["about_info"] = about_info

    #Get the dataset link
    dataset_link = browser.find_element(By.XPATH,'//*[@id="popup-content-0"]/div[1]/a').get_attribute('href')
    res["dataset_link"] = dataset_link
    
    #Find when the dataset was last updated
    # all_dates = []
    # browser.find_element(By.XPATH,'//*[@id="main"]/div/section/div/div/div/div[1]/div/div/div/div/article/div/div[3]/div/div/div/a').click()
    # last_updated = browser.find_element(By.XPATH,'/html/body/footer/div[1]/div').text
    # last_updated = last_updated[15:]
    # last_updated_date = standardize(DATE_FMT,last_updated)

    # res["last_updated"] = last_updated_date

    # #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    # latest_year_available=last_updated_date[-4:]
    # current_date=date.today()
    # current_year=current_date.year
    # year_difference=int(current_year)-int(latest_year_available)
    # status="Active"
    # if year_difference>=5:
    #     status="Inactive"
    # res["dataset_status"] = status

    # res["dataset_file_format"] = ["pdf"]

    #Close and quit all browser driver instances
    browser.quit()

    return res

# result=get_data_attributes()
# print(result)
