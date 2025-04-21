# app/app.py - FINAL VERSION with JSON Response Fix

from flask import Flask, request, jsonify, Response # Added Response
from flask_cors import CORS
from openastrochart.openAstroChart import openAstroChart
import os
# Import traceback for potentially better error logging if needed later
# import traceback

app = Flask(__name__)
CORS(app) # Apply CORS

@app.route('/')
def index():
    '''identify the service'''
    print("--- Handling GET / request ---")
    return 'Web Service for OpenAstro v1.1.57' # Assuming this version string is correct

@app.route('/createchart/', methods=['POST']) # POST only endpoint
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

        # Logging added previously to check keys
        print(f"--- Preparing to call setChartData. Keys in oac dict: {oac.keys()} ---")
        if 'datetime' in oac:
            print(f"--- 'datetime' (lowercase) key FOUND in oac dict. Value: {oac.get('datetime')} ---")
        elif 'dateTime' in oac:
            print(f"--- 'dateTime' (camelCase) key FOUND in oac dict. Value: {oac.get('dateTime')} ---")
        else:
            print("--- WARNING: Neither 'datetime' nor 'dateTime' key found in oac dict (Library might require 'datetime') ---")


        print('--- createchart - creating openAstroChart instance ---')
        chart = openAstroChart ()

        print('--- createchart - calling chart.setChartData with oac dict ---')
        chart.setChartData (oac) # Pass the dictionary
        print('--- createchart - setChartData finished ---')

        print('--- createchart - calling chart.calc() ---')
        chart.calc ()
        print('--- createchart - chart.calc() finished ---')

        print('--- createchart - calling chart.getChartToJSON() ---')
        # This method returns a JSON STRING, not a dictionary
        chart_json_string = chart.getChartToJSON ()
        print('--- createchart - getChartToJSON finished, returning raw JSON string ---')

        # --- FIX: Return the JSON string directly with correct MIME type ---
        # Don't re-encode with jsonify()
        return Response(chart_json_string, mimetype='application/json')
        # --- END FIX ---

    # Keep existing error handling (KeyError and general Exception)
    except KeyError as e:
        print(f"--- ERROR: KeyError in /createchart/: Missing key {e} ---")
        print(f"--- Payload received was: {request.get_json()} ---")
        # print(traceback.format_exc()) # Uncomment for full traceback
        return jsonify({"error": f"Internal error: Missing expected data field '{e}'"}), 500
    except Exception as e:
        print(f"--- ERROR: Unexpected exception in /createchart/: {type(e).__name__} - {e} ---")
        # print(traceback.format_exc()) # Uncomment for full traceback
        return jsonify({"error": "Internal server error during chart calculation"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050)) # Use PORT from environment for Railway
    print(f"--- Starting Flask server on 0.0.0.0:{port} ---")
    # Run with debug=False on Railway
    app.run(host='0.0.0.0', port=port, debug=False)