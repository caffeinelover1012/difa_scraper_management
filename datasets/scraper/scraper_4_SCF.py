from .BaseScraper import *

DATE_FMT = "%m/%d/%Y"
ORG_URL = "https://www.federalreserve.gov/econres/scfindex.htm"
ORGANIZATION = "Survey of Consumer Finances"
DATASET_NAME = "Survey of Consumer Finances (SCF)"
SPONSOR_NAME = "Federal Reserve Board's Division of Research and Statistics"
DATASET_COLLECTION_METHOD = "The survey has contained a panel element over two periods. Respondents to the 1983 survey were re-interviewed in 1986 and 1989. Respondents to the 2007 survey were re-interviewed in 2009.\
                            The study is sponsored by the Federal Reserve Board in cooperation with the Department of the Treasury. Since 1992, data have been collected by the NORC at the University of Chicago. \
                            Participation in the study is strictly voluntary. However, because only about 6,500 families were interviewed in the most recent study, every family selected is very important to the results. To maintain the scientific validity of the study, interviewers are not allowed to substitute respondents for families that do not participate. Thus, if a family declines to participate, it means that families like theirs may not be represented clearly in national discussions."


class SCF(BaseScraper):
    def __init__(self, dataset_id=None):
        super().__init__(dataset_id=dataset_id)
        self.set_date_format(DATE_FMT)
        self.setup_static_attrs({
            'acronym': "SCF",
            'access_type': self.constants['OPEN_ACCESS'],
            'sponsor_name': SPONSOR_NAME,
            'dataset_name': DATASET_NAME,
            'dataset_website_link': ORG_URL,
            'dataset_link': ORG_URL,
            'dataset_collection_method': DATASET_COLLECTION_METHOD
        })

        about_url = "https://www.federalreserve.gov/econres/aboutscf.htm"
        about_soup = self.fetch_data_with_requests(about_url)
        data_soup = self.fetch_data_with_requests(ORG_URL)
        self.extract_data_attributes(about_soup=about_soup, data_soup=data_soup)

        self.finalize_additional_attributes()

    def extract_data_attributes(self, **kwargs):
        super().extract_data_attributes(**kwargs)
        about_soup = kwargs.get('about_soup')
        data_soup = kwargs.get('data_soup')
        
        try:
            self.res['about_info'] = about_soup.find('div', attrs={'id': 'article'}).find('p').get_text()

            table = data_soup.find_all('table', class_='pubtables')
            last_updated = {'CPORT': None, 'STATA': None, 'ASCII': None}
            for t in table:
                if "full public data" in t.find('caption').get_text().lower():
                    rows = t.find_all('tr')
                    for row in rows:
                        row_contents = [i.get_text() for i in row.find_all('td')]
                        if len(row_contents) >= 2:
                            potential_key = row_contents[0].split()[0].upper()
                            if potential_key in last_updated:  # Check for at least 2 cells
                                last_updated[potential_key] = row_contents[-1]
                    break
            self.res['dataset_file_format'] = [format.lower() for format in last_updated.keys()]
            latest_dates = [standardize(DATE_FMT, date) for date in last_updated.values() if date]
            self.res['last_updated'] = max(latest_dates) if latest_dates else None
            self.res['dataset_status'] = 'Retired' if self.res['last_updated'] and is_older_than_5yrs(self.res['last_updated']) else 'Active'
            self.res['other_info'] = "https://www.federalreserve.gov/econres/scf_faqs.htm"

        except Exception as e:
            self.error_out(str(e), self.dataset_id)

    def finalize_additional_attributes(self):
        self.res['dataset_citation'] = f"{self.res['sponsor_name']} (year of release). {self.res['dataset_name']} [Data set]. Retrieved from {self.res['dataset_link']}"
        return None
# ---------------------------------------------------
    # Old code for reference
# ---------------------------------------------------
#
# # Define a function to get the data attributes for an organization
# def get_data_attributes(url):

#     res = {i: "N/A" for i in ATTRS}
#     res['acronym'] = "SCF"
#     res['dataset_website_link'] = url
#     res['access_type'] = 'Open Access'
#     res['sponsor_name'] = "Federal Reserve Board's Division of Research and Statistics"
#     res['dataset_name'] = "Survey of Consumer Finances (SCF)"
#     res['dataset_link'] = "https://www.federalreserve.gov/econres/scfindex.htm"
#     res['dataset_citation'] = f"{res['sponsor_name']} (year of release). {res['dataset_name']} [Data set]. Retrieved from [URL]\n For example, the citation would look like:\n {res['sponsor_name']} (2020). {res['dataset_name']} 2019 [Data set]. Retrieved from {res['dataset_link']}\n"
    
#     DATASET_COLLECTION_METHOD = "The survey has contained a panel element over two periods. Respondents to the 1983 survey were re-interviewed in 1986 and 1989. Respondents to the 2007 survey were re-interviewed in 2009.\
#                                 The study is sponsored by the Federal Reserve Board in cooperation with the Department of the Treasury. Since 1992, data have been collected by the NORC at the University of Chicago. \
#                                 Participation in the study is strictly voluntary. However, because only about 6,500 families were interviewed in the most recent study, every family selected is very important to the results. To maintain the scientific validity of the study, interviewers are not allowed to substitute respondents for families that do not participate. Thus, if a family declines to participate, it means that families like theirs may not be represented clearly in national discussions."
#     res["dataset_collection_method"] = DATASET_COLLECTION_METHOD

    
#     # Make a request to the organization's website
#     response = requests.get(res['dataset_link'])
#     about_link = "https://www.federalreserve.gov/econres/aboutscf.htm"
#     ab_soup = BeautifulSoup(requests.get(about_link).content, 'html.parser')
#     res['about_info'] = ab_soup.find(
#         'div', attrs={'id': 'article'}).find('p').get_text()
    

#     # Parse the HTML content of the response using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#     # about = (soup.find('section', id='primary').find(
#     #     'div').find('p').get_text())
#     # res['about_info'] = about
#     table = soup.find_all('table', class_='pubtables')
#     for t in table:
#         if "full public data" in t.find('caption').get_text().lower():
#             table = t
#             break
#     last_updated = {'SAS': None, 'STATA': None, 'ASCII': None}
#     res['dataset_file_format'] = list(map(lambda x: x.lower(),list(last_updated.keys())))
#     rows = table.find_all('tr')
#     for row in (rows):
#         row_contents = ([i.get_text() for i in row.find_all('td')])
#         if len(row_contents) > 1:
#             if row_contents[0] in last_updated:
#                 last_updated[row_contents[0]] = row_contents[-1]
#     if not STD_FMT == DATE_FMT:
#         for k, v in last_updated.items():
#             last_updated[k] = standardize(DATE_FMT, last_updated[k])
#     res['last_updated'] = get_latest(last_updated.values())

#     res['dataset_status'] = 'Retired' if is_older_than_5yrs(
#         res['last_updated']) else 'Active'
#     res['other_info'] = "https://www.federalreserve.gov/econres/scf_faqs.htm"
#     return res


# # # x = get_data_attributes(FOOD_APS_URL)
# # # print(x)
# # # Loop through the organization dictionary and print the data attribute output
# # print(ORGANIZATION)
# # print('-' * len(ORGANIZATION))
# # data_attributes = get_data_attributes(ORG_URL)
# # for attribute, value in data_attributes.items():
# #     print(f'{attribute}: {value}', end="\n\n")
# # print()
