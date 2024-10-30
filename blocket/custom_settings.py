# custom_settings.py
from scrapy.settings.default_settings import LOG_LEVEL

VACANCY_PAGE_PARSING_ENABLED = True


DOWNLOAD_DELAY = 2
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

DUPEFILTER_CLASS = 'blocket.dupefilters.DatabaseDupeFilter'
#DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

LOG_LEVEL = 'WARNING'