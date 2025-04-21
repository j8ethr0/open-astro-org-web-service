# app/app.py - Add detailed logging before setChartData

from flask import Flask, request, jsonify
from flask_cors import CORS
from openastrochart.openAstroChart import openAstroChart
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    '''identify the service'''
    print("--- Handling GET / request ---")
    return 'Web Service for OpenAstro v1.1.57'

@app.route('/createchart/', methods=['POST']) # Changed back to POST only for clarity
def createchart() :
    '''wrapper to create chart'''
    print("--- Handling /createchart/ request ---")
    try:
        # Directly uses the incoming JSON as the data object 'oac'
        oac = request.json
        if not oac:
             print("--- ERROR: No JSON payload received ---")
             return jsonify({"error": "Missing JSON payload"}), 400

        print(f"--- Received Payload (type: {type(oac)}): {oac} ---") # Log type and content

        # --- ADD DETAILED LOGGING BEFORE LIBRARY CALL ---
        print(f"--- Preparing to call setChartData. Keys in oac dict: {oac.keys()} ---")
        # Explicitly check for both cases just in case
        if 'datetime' in oac:
            print(f"--- 'datetime' (lowercase) key FOUND in oac dict. Value: {oac.get('datetime')} ---")
        elif 'dateTime' in oac:
            print(f"--- 'dateTime' (camelCase) key FOUND in oac dict. Value: {oac.get('dateTime')} ---")
        else:
            # This is the critical point if the error persists
            print("--- CRITICAL WARNING: Neither 'datetime' nor 'dateTime' key found in oac dict before calling setChartData! ---")
        # --- END DETAILED LOGGING ---

        print('--- createchart - creating openAstroChart instance ---')
        chart = openAstroChart ()

        print('--- createchart - calling chart.setChartData with oac dict ---')
        chart.setChartData (oac) # Pass the dictionary
        print('--- createchart - setChartData finished ---') # Will error before here if key missing

        print('--- createchart - calling chart.calc() ---')
        chart.calc ()
        print('--- createchart - chart.calc() finished ---')

        print('--- createchart - calling chart.getChartToJSON() ---')
        chart_json = chart.getChartToJSON ()
        print('--- createchart - getChartToJSON finished, returning JSON ---')

        return jsonify(chart_json)

    # Keep existing error handling (KeyError and general Exception)
    except KeyError as e:
        print(f"--- ERROR: KeyError in /createchart/: Missing key {e} ---")
        print(f"--- Payload received was: {request.get_json()} ---")
        return jsonify({"error": f"Internal error: Missing expected data field '{e}'"}), 500
    except Exception as e:
        print(f"--- ERROR: Unexpected exception in /createchart/: {type(e).__name__} - {e} ---")
        return jsonify({"error": "Internal server error during chart calculation"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"--- Starting Flask server on 0.0.0.0:{port} ---")
    app.run(host='0.0.0.0', port=port, debug=False)