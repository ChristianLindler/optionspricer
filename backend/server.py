#!/usr/bin/env python3
"""
Flask server entry point for local development.
Starts the options pricing API server with debug mode enabled.
"""

import os
import sys

# Load environment variables from .env file FIRST, before any other imports
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, that's fine for production
    pass

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Options Pricer server on http://localhost:{port}")
    print("📊 API endpoint: http://localhost:5000/price_option")
    print("🔧 Debug mode: ON")
    print("📝 Logs will show detailed request/response information")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1) 