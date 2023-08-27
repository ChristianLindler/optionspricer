from flask import Flask, request, jsonify
from optionsPricer import price_option
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
num_sample_paths = 150

# When front end makes POST request, we price option
@app.route('/price_option', methods=['POST'])
def calculate_option_price():
    # Get data
    data = request.get_json()
    call_or_put = data['callOrPut']
    ticker = data['ticker']
    K = int(data['K'])
    T = int(data['T'])
    num_sims = int(data['numSims'])

    option_price, paths = price_option(call_or_put, ticker, K, T, num_sims)
    sample_paths = paths[:num_sample_paths]
    response = {'option_price': option_price,
                'paths': sample_paths}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)