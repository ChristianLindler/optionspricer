"""
Flask API for options pricing service.
Provides REST endpoint for pricing options using Monte Carlo simulation.
"""

from flask import Flask, request, jsonify, make_response
from pricing import price_option
from data.cache import get_api_usage_stats
from flask_cors import CORS
import os

app = Flask(__name__)

# CORS configuration
ALLOWED_ORIGINS = [
    'https://optionspricerapp.com', 
    'https://christianlindler.github.io/optionspricer',
    'http://localhost:3000',  # React dev server
    'http://127.0.0.1:3000'   # Alternative localhost
]
CORS(app, resources={
    r"/price_option": {"origins": ALLOWED_ORIGINS},
    r"/price_option/*": {"origins": ALLOWED_ORIGINS}
})

# Configuration
MAX_SAMPLE_PATHS = 150  # Limit paths sent to frontend for performance


@app.route('/', methods=['OPTIONS'])
def handle_options():
    """Handle preflight OPTIONS requests."""
    return make_response(), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    print("🏥 Health check request received")
    return jsonify({
        'status': 'healthy',
        'message': 'Options pricer API is running',
        'timestamp': '2024-01-01T00:00:00Z'
    })


@app.route('/price_option', methods=['POST'])
def calculate_option_price():
    """
    Calculate option prices using Monte Carlo simulation.
    
    Expected JSON payload (new field names):
    {
        "option_type": "call" | "put",
        "ticker": "AAPL",
        "strike_price": 150.0,
        "time_to_expiry": 30,
        "num_simulations": 1000
    }
    
    Legacy field names also supported:
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
    print(f"🔍 Received request to /price_option from {request.origin}")
    print(f"📝 Request headers: {dict(request.headers)}")
    
    try:
        data = request.get_json()
        print(f"📊 Request data: {data}")
        
        # Support both new and legacy field names
        call_or_put = data.get('option_type', data.get('callOrPut', '')).lower()
        ticker = data.get('ticker', '').upper().strip()
        strike_price = float(data.get('strike_price', data.get('K', 0)))
        time_to_expiry_days = float(data.get('time_to_expiry', data.get('T', 0)))
        num_simulations = int(data.get('num_simulations', data.get('numSims', 0)))
        
        print(f"🎯 Processing: {call_or_put} option for {ticker}, strike=${strike_price}, days={time_to_expiry_days}")
        
        # Convert days to years for the simulation (if needed)
        time_to_expiry_years = time_to_expiry_days / 365.0
        
        # Validate required fields
        if not call_or_put:
            return jsonify({'error': 'Missing required field: option_type or callOrPut'}), 400
        if not ticker:
            return jsonify({'error': 'Missing required field: ticker'}), 400
        if strike_price <= 0:
            return jsonify({'error': 'Missing or invalid required field: strike_price or K'}), 400
        if time_to_expiry_days <= 0:
            return jsonify({'error': 'Missing or invalid required field: time_to_expiry or T'}), 400
        if num_simulations <= 0:
            return jsonify({'error': 'Missing or invalid required field: num_simulations or numSims'}), 400
        
        # Validate input values
        if time_to_expiry_days > 365:  # Max 1 year (365 days)
            return jsonify({'error': 'Time to expiry must be between 0 and 365 days'}), 400
        if num_simulations < 100 or num_simulations > 10000:  # Reduced limits for deployment
            return jsonify({'error': 'Number of simulations must be between 100 and 10,000'}), 400
        if call_or_put not in ['call', 'put']:
            return jsonify({'error': 'Option type must be "call" or "put"'}), 400
        
        # Price the option
        american_price, european_price, american_se, european_se, paths, volatility, dividends = price_option(
            call_or_put, ticker, strike_price, time_to_expiry_years, num_simulations
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
                sampled_paths = [list(p) for p in sampled_paths]
        
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
            'strike_price': strike_price,
            'time_to_expiry': time_to_expiry_days,
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