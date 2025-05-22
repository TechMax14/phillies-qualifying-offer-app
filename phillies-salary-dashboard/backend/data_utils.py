# data_utils.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import re
import logging

# Logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function: fetch_salary_data
# Sends HTTP GET request to the MLB salary URL, parses the HTML table, and returns a DataFrame
def fetch_salary_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Successfully reached salary data URL.")
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if not table:
        logger.error("No <table> element found on the page.")
        return pd.DataFrame()

    try:
        df = pd.read_html(StringIO(str(table)))[0]
        logger.info(f"Parsed salary table with {len(df)} rows.")
        return df
    except ValueError as ve:
        logger.error(f"Failed to convert HTML table to DataFrame: {ve}")
        return pd.DataFrame()

# Function: clean_salary
# Converts a raw salary string (e.g. "$34,000,000") into an integer (e.g. 34000000)
# Returns None for malformed or missing values
def clean_salary(s):
    if not isinstance(s, str):
        return None

    s = s.strip()
    if s.lower() in ["", "no salary data", "nan"]:
        return None

    match = re.search(r'[\d,]+', s.replace('$', ''))
    if not match:
        return None

    try:
        return int(match.group().replace(',', ''))
    except ValueError:
        return None
