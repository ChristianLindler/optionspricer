from flask import Flask, request, jsonify
from options_pricer import price_option
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app, resources={r"/price_option/*": {
    "origins": "https://optionspricerapp.com", 
                                          "allow_headers": ["Content-Type", "Authorization"]}})
num_sample_paths = 150


@app.route('/price_option', methods=['GET', 'OPTIONS'])
def everything_else():
    response = jsonify({'nothing': 'not much'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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

    us_option_price, eu_option_price, paths, us_price_std, eu_price_std, payoff_std = price_option(call_or_put, ticker, K, T, num_sims)
    response = jsonify(
        {
            'us_option_price': us_option_price,
            'eu_option_price': eu_option_price,
            'paths': paths,
            'us_price_std': us_price_std,
            'eu_price_std': eu_price_std,
            'payoff_std': payoff_std,
        }
    )
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)