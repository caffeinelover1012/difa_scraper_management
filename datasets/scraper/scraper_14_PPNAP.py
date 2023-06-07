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
    
    #Sponsor Name
    SPONSOR_NAME = "United States Department of Agriculture (USDA), Agricultural Research Service (ARS)."
    res["sponsor_name"] = SPONSOR_NAME
    
    #Citation Method
    DATASET_CITATION = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']}  [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/105537/pp_national_average_prices_csv.zip?v=5938.6\n"
    res["dataset_citation"] = DATASET_CITATION

    #Type of access to the dataset
    res["access_type"] = "Open Access"

    about_info = "The Purchase to Plate Suite (PP-Suite) is a set of data products developed by linking household and retail grocery scanner data with the USDA Food and Nutrient Database for Dietary Studies (FNDDS), one of USDA’s nutrition databases. The National Average Prices allow users to import price estimates for foods found in USDA dietary survey data. Restricted access elements of the Purchase to Plate Suite include the Crosswalk, Price Tool, and Ingredient Tool. The Purchase to Plate National Average Prices (PP-NAP) for WWEIA/NHANES provides unit price estimates for the foods participants reported eating in What We Eat in America (WWEIA), the dietary component of the National Health and Nutrition Examination Survey (NHANES). The estimates are derived using the Purchase to Plate Crosswalk, the Purchase to Plate Price Tool, and retail grocery scanner data. The primary purpose of the PP-NAP is to support the updates of the market baskets for the USDA Food Plans, including the Thrifty Food Plan. Each price series covers 2 years of data (e.g., 2015/16)."
    #Collect dataset info by redirecting to About this Survey page
    res["about_info"] = about_info

    response = requests.get(ORG_URL)
    soup = BeautifulSoup(response.content,'html.parser')

    #Get the dataset link
    dataset_link = []
    links = soup.find('section',id="primary").find('table').find_all('a')
    default_link = "https://www.ers.usda.gov/"
    for link in links:
        dataset_link.append(default_link + link.get('href'))
    res["dataset_link"] = dataset_link

    #Find when the dataset was last updated
    rows = soup.find('section',id="primary").find('table').find_all('tr')
    all_dates = []
    count = 0
    for row in rows:
        if count==0:
            count+=1
            continue
        cols = row.find_all('td')
        for col in range(len(cols)):
            if col==1:
                dat = cols[col].get_text()
                all_dates.append(standardize(DATE_FMT,dat))
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

    return res