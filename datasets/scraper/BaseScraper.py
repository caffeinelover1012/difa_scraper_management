from datasets.models import Dataset
from .common_imports import *
from .constants import scraper_constants
logger = logging.getLogger(__name__)

class ScrapingError(Exception):
    """Custom exception for scraping errors."""
    pass

class BaseScraper(ABC):
    def __init__(self, dataset_id=None, scraper_constants=scraper_constants):
        self.res = {attr: "N/A" for attr in scraper_constants.get("ATTRS")}
        self.scraper_date_format = scraper_constants.get('STD_FMT')
        self.constants = scraper_constants
        self.dataset_id = dataset_id
        self.config_flags = {'date_format_set':False}

    def error_out(self, error_message, dataset_id):
        if dataset_id:
            Dataset.objects.filter(id=dataset_id).update(is_errored=True)
            logger.error(f"SCRAPER_ERROR on id: {dataset_id} - {error_message}")
        else:
            logger.error(f"SCRAPER_ERROR - {error_message}")
        raise ScrapingError(error_message)
            
    def check_config_flags(self):
        if not self.config_flags.get("date_format_set"):
            raise RuntimeError("Date format must be set in the subclass. Check the Base Scraper Class. Default to STD_FMT.")

    def set_date_format(self, date_format):
        """
        The scraper date format may differ from the standard date format. 
        In order to harmonize data, we check what format the scraper website has the date in, 
        and assign it to scraper_date_format, which defaults to the STD_FMT.
        """
        self.scraper_date_format = date_format
        self.config_flags['date_format_set'] = True

    def setup_static_attrs(self, attrs):
        for key, value in attrs.items():
            try:
                self.res[key] = value
            except KeyError as e:
                self.error_out(str(e), self.dataset_id)
        return None

    def fetch_data_with_requests(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                self.error_out(str(response), self.dataset_id)
        except Exception as e:
                self.error_out(str(e), self.dataset_id)
        return None
        
    def fetch_data_with_selenium(self, url):
        try:
            options = Options()
            options.headless = True
            options.add_argument('--headless=new')
            options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            self.error_out(str(e), self.dataset_id)
        # finally:
            # driver.quit() #IMPORTANT: REMEMBER TO CALL THIS IN DERIVED CLASS 
        return None

    @abstractmethod
    def extract_data_attributes(self, soup=None, driver=None, *args, **kwargs):
        """
        Implement this method in subclasses to extract data from the soup or Selenium driver
        and assign values to self.res
        """
        self.check_config_flags()
    
    @abstractmethod
    def finalize_additional_attributes(self):
        """
        Abstract method to be implemented by each scraper for the specific scraping logic.
        """
        pass

    def get_result(self):
        return self.res