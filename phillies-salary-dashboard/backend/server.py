# server.py
from flask import Flask, jsonify
from flask_cors import CORS
import logging

from data_utils import fetch_salary_data
from logic import compute_qualifying_offer

# Logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Flask app and enable CORS for frontend access
app = Flask(__name__)
CORS(app)

# Route: /api/data
# Fetches live MLB salary data, cleans and computes qualifying offer, and returns structured JSON
@app.route("/api/data", methods=["GET"])
def get_salary_data():
    logger.info("=" * 100)
    logger.info("STEP 1 - Fetching salary data from MLB source...")
    url = "https://questionnaire-148920.appspot.com/swe/data.html"
    df = fetch_salary_data(url)

    if df.empty:
        logger.error("No data returned from MLB source.")
        return jsonify({"error": "Failed to retrieve salary data."}), 500

    logger.info("STEP 2 - Cleaning and computing qualifying offer...")
    qualifying_offer, top_125, cleaned_df = compute_qualifying_offer(df)

    logger.info("STEP 3 - Returning cleaned dataset to frontend")
    return jsonify({
        "qualifying_offer": round(qualifying_offer, 2),
        "top_125": top_125.to_dict(orient="records"),
        "all_players": cleaned_df.to_dict(orient="records")
    })

# Entrypoint: Start Flask development server
if __name__ == "__main__":
    logger.info("Starting Flask backend on http://localhost:5000")
    app.run(debug=True, port=5000)
