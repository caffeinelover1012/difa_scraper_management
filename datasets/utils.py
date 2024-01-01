import logging
import re
import os
import glob
import importlib
from django.conf import settings

logger = logging.getLogger(__name__)

SCRAPER_MAPPING = {}

def refresh_scraper_mapping():
    from .models import Dataset
    
    scraper_files = glob.glob(os.path.join(settings.BASE_DIR, 'datasets', 'scraper', 'scraper_*.py'))
    
    # Regular expression pattern to match 'scraper_num_name.py'
    pattern = re.compile(r'scraper_\d+_[a-zA-Z]+\.py$')
    # print("files",scraper_files)
    for file in scraper_files:
        filename = os.path.basename(file)
    
        # Check if the filename matches the pattern
        if pattern.match(filename):
            module_name = f"datasets.scraper.{filename[:-3]}"
            module = importlib.import_module(module_name)
            scraper_id = int(filename.split("_")[1])
            
            # Retrieve the class name from the module (assuming it's the only class in the module)
            class_name = str(filename[:-3].split("_")[2])
            scraper_class = getattr(module, class_name)
            # Check if a dataset with the scraper_id already exists in the database
            dataset, created = Dataset.objects.get_or_create(pk=scraper_id)

            SCRAPER_MAPPING[scraper_id] = scraper_class

    # print(SCRAPER_MAPPING)

# Returns sraper results
def run_scraper(scraper_id):
    # print("mapping", SCRAPER_MAPPING)
    if scraper_id not in SCRAPER_MAPPING:
        raise ValueError(f'Scraper with ID {scraper_id} not found.')
    scraper_class = SCRAPER_MAPPING[scraper_id]
    try:
        scraper_instance = scraper_class(dataset_id=scraper_id)
        return scraper_instance.get_result()
    except Exception as e:
        logger.error(f"SCRAPER_ERROR in Run Scraper utils.py: {str(e)}")
        return None

# Example usage:
# result, error_occurred = run_scraper(15)
