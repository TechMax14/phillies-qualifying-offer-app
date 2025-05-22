# logic.py
import pandas as pd
from data_utils import clean_salary
import logging

# Logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function: compute_qualifying_offer
# Takes a salary DataFrame, filters for MLB-level players,
# cleans salaries, computes the top 125 earners, and calculates the qualifying offer.
# Returns the qualifying offer (float), top 125 DataFrame, and the cleaned full DataFrame.
def compute_qualifying_offer(df):
    logger.info("Starting salary cleaning and filtering process...")

    # Filter to MLB-level players and clean salary strings
    df = df[df['Level'] == 'MLB'].copy()
    df['CleanedSalary'] = df['Salary'].apply(clean_salary)

    # Identify and log rows with invalid or missing salary values
    invalid_salaries = df[df['CleanedSalary'].isna()]
    logger.info(f"Dropped {len(invalid_salaries)} rows with invalid or missing salary data.")
    
    if not invalid_salaries.empty:
        logger.info("Sample of removed rows:")
        logger.info("\n" + invalid_salaries[['Player', 'Salary']].head(10).to_string(index=False))

    # Filter valid rows and extract top 125 salaries
    df = df.dropna(subset=['CleanedSalary'])
    top_125 = df.sort_values(by='CleanedSalary', ascending=False).head(125)

    # Log top 5 salaries in formatted view
    top_5 = top_125[['Player', 'CleanedSalary']].head().copy()
    top_5['CleanedSalary'] = top_5['CleanedSalary'].apply(lambda x: f"${x:,.0f}")
    logger.info("Top 5 MLB Salaries:")
    logger.info("\n" + top_5.to_string(index=False))

    # Compute the qualifying offer value
    qo = top_125['CleanedSalary'].mean()
    logger.info(f"Computed Qualifying Offer: ${qo:,.2f}")

    return qo, top_125, df
