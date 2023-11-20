from flask import Flask, request, jsonify, make_response
from options_pricer import price_option
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
allowed_origins = ['https://optionspricerapp.com', 'https://christianlindler.github.io/optionspricer']
CORS(app, resources={r"/price_option/*": {"origins": allowed_origins}})
num_sample_paths = 150

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/', methods=['OPTIONS'])
def everything_else():
    return make_response(), 200

# When front end makes POST request, we price option
@app.route('/price_option', methods=['POST'])
def calculate_option_price():
    data = request.get_json()
    call_or_put = data['callOrPut']
    ticker = data['ticker']
    K = float(data['K'])
    T = float(data['T'])
    num_sims = int(data['numSims'])

    us_option_price, eu_option_price, paths, us_price_std, eu_price_std, vol, dividends  = price_option(call_or_put, ticker, K, T, num_sims)
    response = jsonify(
        {
            'us_option_price': us_option_price,
            'eu_option_price': eu_option_price,
            'paths': paths,
            'us_price_std': us_price_std,
            'eu_price_std': eu_price_std,
            'vol': vol,
            'dividends': dividends
        }
    )
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)