from flask import Flask, request, jsonify
from optionsPricer import price_option
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"price_option": {"origins": "http://localhost:3000"}})

num_sample_paths = 150

@app.route('/price_option', methods=['GET', 'OPTIONS'])
@cross_origin()
def everything_else():
    response = jsonify({'nothing': 'not much'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# When front end makes POST request, we price option
@app.route('/price_option', methods=['POST'])
@cross_origin()
def calculate_option_price():
    # Get data
    data = request.get_json()
    call_or_put = data['callOrPut']
    ticker = data['ticker']
    K = int(data['K'])
    T = int(data['T'])
    num_sims = int(data['numSims'])

    option_price, paths, price_std, payoff_std = price_option(call_or_put, ticker, K, T, num_sims)
    sample_paths = paths[:num_sample_paths]
    response = jsonify(
        {
            'option_price': option_price,
            'paths': sample_paths,
            'price_std': price_std,
            'payoff_std': payoff_std,
        }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)