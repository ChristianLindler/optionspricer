"""
Flask API for options pricing service.
Provides REST endpoint for pricing options using Monte Carlo simulation.
"""

from flask import Flask, request, jsonify, make_response
from pricing import price_option
from data.cache import get_api_usage_stats
from flask_cors import CORS
import os

# Try to load .env file for local development, but don't fail if it doesn't exist
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, that's fine for production
    pass

app = Flask(__name__)

# CORS configuration
ALLOWED_ORIGINS = [
    'https://optionspricerapp.com', 
    'https://christianlindler.github.io/optionspricer',
    'http://localhost:3000',  # React dev server
    'http://127.0.0.1:3000'   # Alternative localhost
]
CORS(app, resources={r"/price_option/*": {"origins": ALLOWED_ORIGINS}})

# Configuration
MAX_SAMPLE_PATHS = 150  # Limit paths sent to frontend for performance


@app.route('/', methods=['OPTIONS'])
def handle_options():
    """Handle preflight OPTIONS requests."""
    return make_response(), 200


@app.route('/price_option', methods=['POST'])
def calculate_option_price():
    """
    Calculate option prices using Monte Carlo simulation.
    
    Expected JSON payload:
    {
        "callOrPut": "call" | "put",
        "ticker": "AAPL",
        "K": 150.0,
        "T": 0.25,
        "numSims": 1000
    }
    
    Returns:
        JSON response with option prices, paths, and metadata
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['callOrPut', 'ticker', 'K', 'T', 'numSims']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract and validate parameters
        call_or_put = data['callOrPut'].lower()
        ticker = data['ticker'].upper().strip()
        strike_price = float(data['K'])
        time_to_expiry = float(data['T'])
        num_simulations = int(data['numSims'])
        
        # Validate input values
        if strike_price <= 0:
            return jsonify({'error': 'Strike price must be positive'}), 400
        if time_to_expiry <= 0 or time_to_expiry > 1.0:  # Max 1 year (365 days)
            return jsonify({'error': 'Time to expiry must be between 0 and 1 year'}), 400
        if num_simulations < 100 or num_simulations > 10000:  # Reduced limits for deployment
            return jsonify({'error': 'Number of simulations must be between 100 and 10,000'}), 400
        if call_or_put not in ['call', 'put']:
            return jsonify({'error': 'Option type must be "call" or "put"'}), 400
        
        # Price the option
        american_price, european_price, american_se, european_se, paths, volatility, dividends = price_option(
            call_or_put, ticker, strike_price, time_to_expiry, num_simulations
        )
        
        # Get API usage statistics
        api_stats = get_api_usage_stats()
        
        # Sample paths for frontend (limit for performance)
        if not hasattr(paths, '__len__') or isinstance(paths, (float, int)):
            sampled_paths = []
        else:
            sampled_paths = paths[:MAX_SAMPLE_PATHS] if len(paths) > MAX_SAMPLE_PATHS else paths
            # Ensure sampled_paths is a list of lists for JSON serialization
            if hasattr(sampled_paths, 'tolist'):
                sampled_paths = sampled_paths.tolist()
            else:
                sampled_paths = [p.tolist() if hasattr(p, 'tolist') else list(p) for p in sampled_paths]
        
        response = jsonify({
            'us_option_price': american_price,
            'eu_option_price': european_price,
            'paths': sampled_paths,
            'us_price_std': american_se,
            'eu_price_std': european_se,
            'vol': volatility,
            'dividends': dividends,
            'api_usage': api_stats,
            'ticker': ticker,
            'strike': strike_price,
            'time_to_expiry': time_to_expiry,
            'option_type': call_or_put,
            'total_paths': len(paths) if hasattr(paths, '__len__') else 0,
            'sampled_paths': len(sampled_paths)
        })
        
        return response
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({
            'error': 'Error calculating option price. Please check the ticker symbol and try again.',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)