#!/usr/bin/env python3
"""
Setup script to help create .env file with required API keys.
"""

import os

def create_env_file():
    """Create a .env file with user input for API keys."""
    
    print("=== Options Pricer Environment Setup ===")
    print("This script will help you create a .env file with your API keys.")
    print("You'll need API keys from:")
    print("1. Alpha Vantage: https://www.alphavantage.co/support/#api-key")
    print("2. Twelve Data: https://twelvedata.com/")
    print()
    
    # Get API keys from user
    alphavantage_key = input("Enter your Alpha Vantage API key: ").strip()
    twelve_key = input("Enter your Twelve Data API key: ").strip()
    
    # Optional Supabase configuration
    print("\nSupabase configuration (optional - press Enter to use defaults):")
    supabase_url = input("Supabase URL (or press Enter for default): ").strip()
    supabase_key = input("Supabase Key (or press Enter for default): ").strip()
    
    # Create .env content
    env_content = f"""# API Keys (Required)
ALPHAVANTAGE_API_KEY={alphavantage_key}
TWELVE_API_KEY={twelve_key}

# Supabase Configuration (Optional - has defaults)
"""
    
    if supabase_url:
        env_content += f"SUPABASE_URL={supabase_url}\n"
    if supabase_key:
        env_content += f"SUPABASE_KEY={supabase_key}\n"
    
    # Write to .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created at: {env_path}")
    print("You can now run the application!")
    print("\nNote: Make sure .env is in your .gitignore to keep your API keys secure.")

if __name__ == "__main__":
    create_env_file() 