from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.ers.usda.gov/data-products/purchase-to-plate/"
ORGANIZATION = "PP-NAP"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "Purchase to Plate National Average Prices (PP-NAP)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = '''The datasets (described below) used to build PP-NAP are USDA’s What We Eat in America (WWEIA), the dietary component of the National Health and Nutrition Examination Survey (NHANES), the USDA Food and Nutrient Database for Dietary Studies (FNDDS), the Information Resources, Inc. (IRI) retail grocery scanner data, and the Purchase to Plate Crosswalk (PPC). The generalized process for construction of the national average prices is as follows:\n
    \n1. Select USDA food codes representing foods or beverages that were reported 10 or more times in the WWEIA cycle, or are needed for the Thrifty Food Plan (TFP) market basket update.
    \n2. Review recipes in the FNDDS of the selected foods to determine whether recipe modifications are needed to accommodate convenience foods and include standard substitutions in the recipe.
    \n3. Calculate the total purchase weight sold and expenditure for each item in the IRI data.
    \n4. Link scanner data Universal Product Codes (UPCs) (barcodes) to food codes in the USDA nutrition databases using the PPC.
    \n5. Convert purchase weight to edible weight for each UPC using the PPC conversion factors.
    \n6. Sum the total expenditure and edible weight across UPCs for each USDA food code.
    \n7. Calculate the average price per 100 grams of the USDA food codes by dividing expenditure by edible weight.
    \n8. Apply average unit prices for the USDA food codes to the recipes identified in step two and calculate the unit price of the FNDDS foods selected in step one.
    \n\nThe resulting prices are nationally representative of foods reported eaten by WWEIA/NHANES participants. The resulting price for any particular food may be derived from multiple brands and private labels, package sizes, flavors, and types. The IRI grocery scanner data represent individual products as purchased in a grocery store. The WWEIA/NHANES codes and supporting recipes in the FNDDS are more general (e.g., BBQ sauce versus a brand-specific BBQ sauce).'''

    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "To cite the Purchase to Plate National Average Prices for WWEIA/NHANES dataset in APA format in your research paper, you can use the following citation format:\n\nU.S. Department of Agriculture, Agricultural Research Service. (year). Purchase to Plate National Average Prices for WWEIA/NHANES Foods [Data set]. Retrieved from [URL].\n\nFor example, in your reference list, the citation would look like this::\n\nU.S. Department of Agriculture, Agricultural Research Service. (2017). Purchase to Plate National Average Prices for WWEIA/NHANES Foods. Retrieved from https://www.ars.usda.gov/ARSUserFiles/80400525/pdf/DBrief/10_prices_national_wweia_2007-08.pdf\n\nMake sure to replace the URL with the specific URL of the dataset you used and the date of access with the date you accessed the dataset. Additionally, if there are specific tables or variables you used, you should include those in your citation as well."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "United States Department of Agriculture (USDA), Agricultural Research Service (ARS)."
    res["sponsor_name"] = SPONSOR_NAME

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
    overview_info =  browser.find_elements(By.XPATH,'//*[@id="primary"]/div/p[*]')
    i = 1
    for info in overview_info:
        if i > 2:
            break
        about_info += info.text + "\n\n"
    #Collect dataset info by redirecting to About this Survey page
    res["about_info"] = about_info

    #Get the dataset link
    dataset_link = []
    links = browser.find_elements(By.XPATH,'//*[@id="primary"]/table/tbody/tr[*]/td[*]/a')
    for link in links:
        dataset_link.append(link.get_attribute('href'))
    res["dataset_link"] = dataset_link 

    #Find when the dataset was last updated
    all_dates = []
    dates = browser.find_elements(By.XPATH,'//*[@id="primary"]/table/tbody/tr[*]/td[2]')
    for dat in dates:
        all_dates.append(standardize(DATE_FMT,dat.text))

    last_updated_date = min(all_dates)
    res["last_updated"] = last_updated_date

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=last_updated_date[-4:]
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"]=status

    res["dataset_file_format"]=["csv","xlsx"]

    #Close and quit all browser driver instances
    browser.quit()

    return res
