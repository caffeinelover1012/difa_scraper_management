from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://nielseniq.com/global/en/solutions/homescan/"
ORGANIZATION = "WWEIA"

# Define a function to get the data attributes for an organization
def get_data_attributes():

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "NIQ Homescan"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = "The Nielsen Homescan dataset is collected using a panel of households who are given a handheld scanner or use a mobile app to scan the barcodes of the products they purchase. The panel is representative of the general population and households are chosen to participate based on their demographics. Panel members are typically given incentives such as cash, gift cards, or free products to encourage participation. The data collected includes information on the products purchased, prices paid, where the products were purchased, and other demographic information about the household. This data is then aggregated and analyzed to provide insights into consumer behavior and market trends."
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Nielsen Homescan dataset in APA format in your research paper, you can use the following citation format:\n\nNielsen (Year). Homescan [Dataset]. NielsenIQ. Retrieved from [URL]. \n\nFor example, in your reference list, the citation would look like this::\n\nNielsen. (2018). Homescan. [Dataset]. NielsenIQ. https://www.nielsen.com/us/en/solutions/capabilities/homescan.html\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
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

    about_info = "Nielsen Homescan dataset tracks, diagnose, and analyze consumer behavior from more than 250,000 households across 25 countries. NielsenIQ helps in understanding consumer behavior across all outlets in order to guide in making decisions for attracting new shoppers and encouraging existing shoppers to buy more."
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

result=get_data_attributes()
print(result)
