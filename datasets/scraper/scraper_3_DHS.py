from .common_imports import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://dhsprogram.com/"
ORGANIZATION = "DHS"

# Define a function to get the data attributes for an organization
def get_data_attributes(url):

    res = {i: "N/A" for i in ATTRS}
    res['dataset_name']="Demographic Health Survey (DHS)"
    res['dataset_website_link'] = ORG_URL

    DATASET_COLLECTION_METHOD = "The basic approach of The DHS Program is to collect data that are comparable across countries. To achieve this, standard model questionnaires have been developed, along with a written description of why certain questions or sections have been included. These model questionnaires—which have been reviewed and modified in each of the seven phases of The DHS Program—form the basis for the questionnaires that are applied in each country. Typically, a country is asked to adopt the model questionnaire in its entirety, but can add questions of particular interest. However, questions in the model can be deleted if they are irrelevant in a particular country. There are two types of DHS surveys:\
                                Standard DHS Surveys have large sample sizes (usually between 5,000 and 30,000 households) and typically are conducted about every 5 years, to allow comparisons over time.\
                                Interim DHS Surveys focus on the collection of information on key performance monitoring indicators but may not include data for all impact evaluation measures (such as mortality rates). These surveys are conducted between rounds of DHS surveys and have shorter questionnaires than DHS surveys. Although nationally representative, these surveys generally have smaller samples than DHS surveys. \
                                DHS surveys collect primary data using four types of Model Questionnaires. A Household Questionnaire is used to collect information on characteristics of the household's dwelling unit and characteristics of usual residents and visitors. It is also used to identify members of the household who are eligible for an individual interview. Eligible respondents are then interviewed using an Individual Woman's or Man's Questionnaire. The Biomarker Questionnaire is used to collect biomarker data on children, women, and men. For special information on topics that are not contained in the Model Questionnaires, optional Questionnaire Modules are available. Interviews are conducted only if the respondent provides voluntary informed consent. " 
    res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    res['access_type'] = 'Restricted Access'
    res['sponsor_name'] = "United States Agency for International Development (USAID)"

    res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from https://www.ers.usda.gov/webdocs/DataFiles/50980/SAS%20data%20files.zip?v=9778.8"
    
    res['dataset_link'] = 'https://dhsprogram.com/data/available-datasets.cfm'
    # Make a request to the organization's website
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    overview = "Demographic and Health Surveys (DHS) are nationally-representative household surveys that provide data for a wide range of monitoring and impact evaluation indicators in the areas of population, health, and nutrition. "
    about = (soup.find('h3', attrs={"class":'HomeBanner__message-text'}).get_text())
    res['about_info'] = overview + about
    curr_date = date.today()
    last_updated = str(curr_date.month)+'/'+str(curr_date.day)+'/'+str(curr_date.year)
    last_updated_date=standardize(DATE_FMT,last_updated)
    res["last_updated"]=last_updated_date
    res["dataset_status"]= "Active"
    res['dataset_file_format'] = ["ASCII", "STATA (.dta,.do,.dct)", "SPSS (.sav,.sps)", "SAS (.sas,.sas7bdat)",".DBF",".MDB"]
    return res
