from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://data.nal.usda.gov/dataset/what-we-eat-america-wweia-database"
ORGANIZATION = "WWEIA"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}

    res["dataset_name"] = "What We Eat In America (WWEIA)"
    res["dataset_website_link"] = ORG_URL

    #Dataset Collection Method
    DATASET_COLLECTION_METHOD = '''Two days of 24-hour dietary recall data are collected in WWEIA, NHANES. The Day 1 interview is conducted in person in the Mobile Examination Center (MEC). The Day 2 interview is collected by telephone 3 to 10 days later, but not on the same day of the week as the Day 1 interview. 
                                \n\nTrained interviewers using the 5-step USDA Automated Multiple-Pass Method (AMPM) collect dietary intakes. The AMPM includes an extensive compilation of standardized food-specific questions and possible response options. Routing of questions is based on previous response. The AMPM is revised for each 2-year collection of WWEIA to reflect the changing food supply. Read more about the AMPM. 
                                \n\nDuring the 24-hour recall, respondents estimate the amount of food and beverages consumed using 3-dimentional models on Day 1 and the USDAs Food Model Booklet on Day 2.'''
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    #Citation Method
    DATASET_CITATION = "U.S. Department of Agriculture, Agricultural Research Service, Beltsville Human Nutrition Research Center, Food Surveys Research Group (Beltsville, MD) and U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, National Center for Health Statistics (Hyattsville, MD). What We Eat in America, NHANES YYYY-YYYY Type of File: Descriptive Name of File (FILENAME). (YYYY, Month). Available from: http://www.cdc.gov/remainder_of_url.xxx [accessed MM/DD/YY]."
    res["dataset_citation"] = DATASET_CITATION

    #Sponsor Name
    SPONSOR_NAME = "U.S. Department of Agriculture (USDA) and the U.S. Department of Health and Human Services (DHHS)"
    res["sponsor_name"] = SPONSOR_NAME

    #Type of access to the dataset
    res["access_type"] = "Open Access"

    about_info = "What We Eat in America (WWEIA), NHANES is a national food survey conducted as a partnership between the U.S. Department of Health and Human Services (HHS) and the U.S. Department of Agriculture (USDA). WWEIA represents the integration of two nationwide surveys - USDA's Continuing Survey of Food Intakes by Individuals (CSFII) and HHS' NHANES. Under the integrated framework, HHS is responsible for the sample design and data collection. USDA is responsible for the survey's dietary data collection methodology, development and maintenance of the food and nutrient databases used to code and process the data. The two surveys were integrated in 2002."
    res["about_info"] = about_info

    #Get the dataset link
    dataset_link = "https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/wweianhanes-overview/"
    res["dataset_link"] = dataset_link
    
    response = requests.get(dataset_link)
    soup = BeautifulSoup(response.content,'html.parser')

    #Find when the dataset was last updated
    last_updated = soup.find('div',class_="page-last-modified").get_text().strip().replace('\n',"")
    last_updated = last_updated[15:]
    last_updated_date = standardize(DATE_FMT,last_updated)

    res["last_updated"] = last_updated_date

    #Find the lastest available year data and compute if the last collected is not more than 5 years of duration.
    latest_year_available=last_updated_date[-4:]
    current_date=date.today()
    current_year=current_date.year
    year_difference=int(current_year)-int(latest_year_available)
    status="Active"
    if year_difference>=5:
        status="Inactive"
    res["dataset_status"] = status

    res["dataset_file_format"] = ["pdf"]

    return res