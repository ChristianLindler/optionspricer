#!/usr/bin/env python3
"""
Test script for the options pricing functionality.
Validates the pricing models and data fetching capabilities.
"""

from pricing import price_option


def test_pricing():
    """Test the pricing function with a realistic example."""
    try:
        print("🧪 Testing Options Pricing Logic")
        print("=" * 50)
        
        # Test with Verizon (dividend-paying stock)
        print("Testing VZ call option:")
        print("  Strike: $40.0")
        print("  Time to expiry: 1.0 years")
        print("  Simulations: 5,000")
        
        try:
            us_price, eu_price, us_std, eu_std, paths, vol, dividends = price_option(
                call_or_put='call',
                ticker='VZ',
                K=40.0,
                T=1.0,
                num_sims=5000
            )
            
            print("\n✅ Pricing Results:")
            print(f"American Option Price: ${us_price:.4f}")
            print(f"European Option Price: ${eu_price:.4f}")
            print(f"American Standard Error: ${us_std:.4f}")
            print(f"European Standard Error: ${eu_std:.4f}")
            print(f"Volatility: {vol:.4f}")
            print(f"Number of paths: {len(paths)}")
            
            # Check if prices are reasonable
            if us_price <= 0 or eu_price <= 0:
                print("❌ Pricing test failed: Option prices should be positive")
                return False
            
            if vol <= 0 or vol > 1:
                print("❌ Pricing test failed: Volatility seems unusual (expected 5%-100%)")
                return False
            
            # For dividend-paying stocks, American should be >= European
            if us_price < eu_price:
                print("❌ Pricing test failed: American price should be >= European price")
                return False
            
            print("\n🎉 VZ test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ VZ pricing test failed: {str(e)}")
            return False
        
        # Test with TSLA (non-dividend stock)
        print("\nTesting TSLA call option (non-dividend stock):")
        print("  Strike: $200.0")
        print("  Time to expiry: 0.5 years")
        print("  Simulations: 5,000")
        
        try:
            us_price, eu_price, us_std, eu_std, paths, vol, dividends = price_option(
                call_or_put='call',
                ticker='TSLA',
                K=200.0,
                T=0.5,
                num_sims=5000
            )
            
            print("\n✅ TSLA Pricing Results:")
            print(f"American Option Price: ${us_price:.4f}")
            print(f"European Option Price: ${eu_price:.4f}")
            print(f"American Standard Error: ${us_std:.4f}")
            print(f"European Standard Error: ${eu_std:.4f}")
            print(f"Volatility: {vol:.4f}")
            print(f"Number of paths: {len(paths)}")
            
            # For non-dividend stocks, American and European should be identical
            price_diff = abs(us_price - eu_price)
            if price_diff > 0.01:  # Allow small numerical differences
                print(f"❌ TSLA test failed: American and European prices should be identical for non-dividend stocks")
                print(f"   Price difference: ${price_diff:.4f}")
                return False
            
            print("\n🎉 TSLA test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ TSLA pricing test failed: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ Pricing test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pricing() 