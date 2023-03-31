# utils.py
import os, glob
import importlib

SCRAPER_MAPPING = {}

def initialize_scraper_mapping():
    scraper_files = glob.glob(('/scraper/scraper_*.py'))

    for file in scraper_files:
        filename = os.path.basename(file)
        module_name = f"datasets.scraper.{filename[:-3]}"
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_data_attributes') and hasattr(module, 'ORG_URL'):
            SCRAPER_MAPPING[filename[:-3]] = (module.get_data_attributes, module.ORG_URL)


initialize_scraper_mapping()

# utils.py
def run_scraper(scraper_id):
    if scraper_id not in SCRAPER_MAPPING:
        raise ValueError(f'Scraper with ID {scraper_id} not found.')
    scrape_function, input_param = SCRAPER_MAPPING[scraper_id]
    return scrape_function(input_param)  # Pass the URL to the scrape function
