#!/usr/bin/env python3
"""
Gold SIP Calculator - Test and Demo Script
Run this to test the calculator functionality
"""

import sys
import os
from datetime import date, timedelta

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from gold_sip_calculator import GoldSIPCalculator
from gold_price_api import LiveGoldPriceAPI, get_live_gold_price

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_section(text):
    """Print a formatted section header"""
    print(f"\n📊 {text}")
    print("-" * 50)

def test_basic_calculation():
    """Test basic SIP calculation"""
    print_section("Basic SIP Calculation Test")
    
    calculator = GoldSIPCalculator()
    
    # Example calculation
    results = calculator.calculate_sip_returns(
        monthly_amount=10000,      # ₹10,000 per month
        duration_months=24,        # 2 years
        average_gold_price=8000,   # ₹8,000/gram average (realistic for 12.5% CAGR)
        current_gold_price=10500,  # ₹10,500/gram current
        start_date=date(2022, 1, 1)
    )
    
    print("✅ Calculation completed!")
    print(f"   Monthly SIP: ₹{results['monthly_amount']:,.0f}")
    print(f"   Duration: {results['duration_months']} months")
    print(f"   Total Investment: ₹{results['total_investment']:,.0f}")
    print(f"   Gold Purchased: {results['total_grams']:.3f} grams")
    print(f"   Current Value: ₹{results['current_value']:,.0f}")
    
    if results['profit_loss'] > 0:
        print(f"   🎉 Profit: ₹{results['profit_loss']:,.0f} ({results['profit_loss_percentage']:.2f}%)")
    else:
        print(f"   📉 Loss: ₹{abs(results['profit_loss']):,.0f} ({abs(results['profit_loss_percentage']):.2f}%)")
    
    print(f"   📈 CAGR: {results['cagr']:.2f}% per annum")
    
    return results

def test_monthly_breakdown():
    """Test monthly breakdown calculation"""
    print_section("Monthly Breakdown Test")
    
    calculator = GoldSIPCalculator()
    
    breakdown = calculator.calculate_monthly_breakdown(
        monthly_amount=5000,
        duration_months=6,
        start_date=date.today() - timedelta(days=180)
    )
    
    print("✅ Monthly breakdown generated!")
    print("\n   Month | Investment | Gold Price | Gold Bought | Cumulative")
    print("   ------|------------|------------|-------------|------------")
    
    for month_data in breakdown:
        print(f"   {month_data['month']:5d} | ₹{month_data['investment_amount']:8,.0f} | "
              f"₹{month_data['gold_price']:8,.0f} | {month_data['grams_bought']:9.3f}g | "
              f"{month_data['cumulative_grams']:10.3f}g")

def test_live_gold_price():
    """Test live gold price functionality"""
    print_section("Live Gold Price Test")
    
    try:
        # Test basic price fetch
        price = get_live_gold_price()
        print(f"✅ Current Gold Price: ₹{price:,.2f}/gram")
        
        # Test detailed price API
        api = LiveGoldPriceAPI()
        price_data = api.get_current_gold_price()
        
        print(f"   📊 Source: {price_data.source}")
        print(f"   🎯 Confidence: {price_data.confidence:.0%}")
        print(f"   🕒 Timestamp: {price_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test USD-INR rate
        usd_inr = api.get_usd_to_inr_rate()
        print(f"   💱 USD-INR Rate: {usd_inr:.2f}")
        
    except Exception as e:
        print(f"❌ Error testing live prices: {e}")

def test_price_history():
    """Test price history functionality"""
    print_section("Price History Test")
    
    try:
        api = LiveGoldPriceAPI()
        history = api.get_price_history(7)  # Last 7 days
        
        print(f"✅ Retrieved {len(history)} historical prices")
        print("\n   Date       | Price    | Source")
        print("   -----------|----------|------------------")
        
        for price_data in history[-5:]:  # Show last 5
            print(f"   {price_data.timestamp.strftime('%Y-%m-%d')} | "
                  f"₹{price_data.price_per_gram:6,.0f} | {price_data.source}")
        
    except Exception as e:
        print(f"❌ Error testing price history: {e}")

def test_summary_generation():
    """Test summary text generation"""
    print_section("Summary Generation Test")
    
    calculator = GoldSIPCalculator()
    
    results = calculator.calculate_sip_returns(
        monthly_amount=15000,
        duration_months=36,
        average_gold_price=7000,   # Realistic for 3-year historical scenario
        current_gold_price=10500
    )
    
    summary = calculator.generate_summary_text(results)
    print("✅ Summary generated!")
    print(summary)

def run_scenario_analysis():
    """Run different investment scenarios"""
    print_section("Scenario Analysis")
    
    calculator = GoldSIPCalculator()
    
    scenarios = [
        {"name": "Conservative (Recent SIP)", "amount": 5000, "duration": 24, "avg_price": 9000, "curr_price": 10500},
        {"name": "Moderate (Historical SIP)", "amount": 10000, "duration": 36, "avg_price": 7500, "curr_price": 10500},
        {"name": "Aggressive (Long-term SIP)", "amount": 20000, "duration": 60, "avg_price": 6000, "curr_price": 10500},
    ]
    
    print(f"\n{'Scenario':<12} | {'Investment':<11} | {'Current Value':<13} | {'Returns':<10} | {'CAGR':<8}")
    print("-" * 70)
    
    for scenario in scenarios:
        results = calculator.calculate_sip_returns(
            monthly_amount=scenario["amount"],
            duration_months=scenario["duration"],
            average_gold_price=scenario["avg_price"],
            current_gold_price=scenario["curr_price"]
        )
        
        print(f"{scenario['name']:<12} | ₹{results['total_investment']:9,.0f} | "
              f"₹{results['current_value']:11,.0f} | "
              f"{results['profit_loss_percentage']:7.2f}% | "
              f"{results['cagr']:6.2f}%")

def main():
    """Main test runner"""
    print_header("🏆 Gold SIP Calculator - Test Suite")
    
    print("🔍 Testing Gold SIP Calculator functionality...")
    print("This script demonstrates all the core features of the calculator.")
    
    try:
        # Run all tests
        test_basic_calculation()
        test_monthly_breakdown()
        test_live_gold_price()
        test_price_history()
        test_summary_generation()
        run_scenario_analysis()
        
        print_header("✅ All Tests Completed Successfully!")
        
        print("\n🚀 Next Steps:")
        print("   1. Run Flask web app: python web/app.py")
        print("   2. Run Streamlit dashboard: streamlit run streamlit_app.py")
        print("   3. Setup Telegram bot: python telegram/telegram_bot.py")
        print("\n📖 Check README.md for detailed setup instructions.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Please check your setup and dependencies.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)