# Your provided app.py (simplified)
from flask import Flask, request, jsonify
from flask_cors import CORS
from openastrochart.openAstroChart import openAstroChart
import os # Make sure os is imported if used later

app = Flask(__name__)
CORS(app) # Apply CORS

@app.route('/')
def index():
    '''identify the service'''
    return 'Web Service for OpenAstro v1.1.57' # Version seems different from repo?

# Route definition - uses trailing slash, accepts GET/POST (though POST is needed)
@app.route('/createchart/', methods=['GET', 'POST'])
def createchart() :
    '''wrapper to create chart'''
    # Directly uses the incoming JSON as the data object 'oac'
    oac   = request.json
    print ('createchart - creating openAstroChart')
    chart = openAstroChart ()
    print ('createchart - importing JSON string to openAstroChart')
    # Passes the entire incoming JSON object to the library
    chart.setChartData (oac)
    print ('createchart - calc chart')
    chart.calc ()
    print ('createchart - convert chart back to JSON and return')
    chart_json = chart.getChartToJSON ()
    return jsonify(chart_json)

if __name__ == '__main__':
    # Using Flask's development server
    # Make sure PORT environment variable is handled for Railway
    port = int(os.environ.get('PORT', 5050)) # Default to 5050 if PORT not set
    # Use host='0.0.0.0' to listen on all interfaces in Docker
    app.run(host='0.0.0.0', port=port, debug=False) # Turn Debug OFF for Railway