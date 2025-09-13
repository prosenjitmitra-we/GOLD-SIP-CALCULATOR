"""
Gold SIP Calculator - Core calculation logic
"""

import datetime
from typing import Dict, List, Tuple
import requests
import json


class GoldSIPCalculator:
    """
    Core calculator for Gold SIP (Systematic Investment Plan) calculations
    """
    
    def __init__(self):
        self.gold_prices_cache = {}
    
    def calculate_sip_returns(
        self,
        monthly_amount: float,
        duration_months: int,
        average_gold_price: float,
        current_gold_price: float,
        start_date: datetime.date = None
    ) -> Dict:
        """
        Calculate Gold SIP returns
        
        Args:
            monthly_amount: Monthly SIP investment amount in INR
            duration_months: Investment duration in months
            average_gold_price: Average gold price during investment period (INR per gram)
            current_gold_price: Current gold price (INR per gram)
            start_date: SIP start date (optional)
        
        Returns:
            Dictionary with calculation results
        """
        
        # Calculate total investment
        total_investment = monthly_amount * duration_months
        
        # Calculate total grams purchased
        total_grams = monthly_amount / average_gold_price * duration_months
        
        # Calculate current value
        current_value = total_grams * current_gold_price
        
        # Calculate profit/loss
        profit_loss = current_value - total_investment
        profit_loss_percentage = (profit_loss / total_investment) * 100
        
        # Calculate CAGR (Compound Annual Growth Rate)
        years = duration_months / 12
        if years > 0:
            cagr = ((current_value / total_investment) ** (1/years) - 1) * 100
        else:
            cagr = 0
        
        return {
            'monthly_amount': monthly_amount,
            'duration_months': duration_months,
            'total_investment': total_investment,
            'average_gold_price': average_gold_price,
            'current_gold_price': current_gold_price,
            'total_grams': round(total_grams, 3),
            'current_value': round(current_value, 2),
            'profit_loss': round(profit_loss, 2),
            'profit_loss_percentage': round(profit_loss_percentage, 2),
            'cagr': round(cagr, 2),
            'start_date': start_date,
            'end_date': start_date + datetime.timedelta(days=duration_months*30) if start_date else None
        }
    
    def calculate_monthly_breakdown(
        self,
        monthly_amount: float,
        duration_months: int,
        gold_prices: List[float] = None,
        start_date: datetime.date = None
    ) -> List[Dict]:
        """
        Calculate month-wise breakdown of SIP investment
        
        Args:
            monthly_amount: Monthly SIP amount
            duration_months: Duration in months
            gold_prices: List of gold prices for each month
            start_date: Investment start date
        
        Returns:
            List of monthly investment details
        """
        
        if not gold_prices:
            # Use realistic gold price progression reflecting historical growth
            base_price = 7500  # Starting price for realistic historical scenario
            # Approximate 12.5% annual growth = 1% monthly growth
            gold_prices = [base_price * (1 + 0.01 * i) for i in range(duration_months)]
        
        monthly_breakdown = []
        cumulative_grams = 0
        cumulative_investment = 0
        
        for month in range(duration_months):
            month_date = start_date + datetime.timedelta(days=month*30) if start_date else None
            gold_price = gold_prices[month] if month < len(gold_prices) else gold_prices[-1]
            
            # Calculate grams bought this month
            grams_bought = monthly_amount / gold_price
            cumulative_grams += grams_bought
            cumulative_investment += monthly_amount
            
            monthly_breakdown.append({
                'month': month + 1,
                'date': month_date,
                'investment_amount': monthly_amount,
                'gold_price': gold_price,
                'grams_bought': round(grams_bought, 3),
                'cumulative_grams': round(cumulative_grams, 3),
                'cumulative_investment': cumulative_investment
            })
        
        return monthly_breakdown
    
    def get_live_gold_price(self) -> float:
        """
        Fetch live gold price from API
        
        Returns:
            Current gold price in INR per gram
        """
        try:
            # Using a mock API endpoint - replace with actual gold price API
            # Example APIs: MetalPriceAPI, CurrencyLayer, etc.
            
            # Mock implementation - returns a realistic gold price
            # In production, replace this with actual API call
            mock_price = 10500 + (datetime.datetime.now().day * 10)  # Varies by day
            
            return mock_price
            
        except Exception as e:
            print(f"Error fetching live gold price: {e}")
            return 10500  # Default fallback price
    
    def format_currency(self, amount: float) -> str:
        """Format currency in Indian format"""
        return f"₹{amount:,.2f}"
    
    def format_weight(self, grams: float) -> str:
        """Format weight in grams"""
        return f"{grams:.3f} grams"
    
    def generate_summary_text(self, results: Dict) -> str:
        """
        Generate human-readable summary of SIP calculation
        
        Args:
            results: Results from calculate_sip_returns()
        
        Returns:
            Formatted summary text
        """
        
        summary = f"""
🏆 **Gold SIP Investment Summary**

💰 **Investment Details:**
• Monthly SIP: {self.format_currency(results['monthly_amount'])}
• Duration: {results['duration_months']} months
• Total Invested: {self.format_currency(results['total_investment'])}

📊 **Gold Purchase:**
• Average Gold Price: {self.format_currency(results['average_gold_price'])}/gram
• Total Gold Purchased: {self.format_weight(results['total_grams'])}

💎 **Current Status:**
• Current Gold Price: {self.format_currency(results['current_gold_price'])}/gram
• Current Value: {self.format_currency(results['current_value'])}

📈 **Returns:**
• Profit/Loss: {self.format_currency(results['profit_loss'])} ({results['profit_loss_percentage']:.2f}%)
• CAGR: {results['cagr']:.2f}% per annum

{'🎉 Congratulations! Your investment is in profit.' if results['profit_loss'] > 0 else '📉 Your investment is currently at a loss, but gold is a long-term investment.'}
        """
        
        return summary.strip()


class GoldPriceAPI:
    """
    Integration with external gold price APIs
    """
    
    @staticmethod
    def fetch_historical_prices(start_date: datetime.date, end_date: datetime.date) -> List[float]:
        """
        Fetch historical gold prices for a date range
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            List of historical gold prices
        """
        
        # Mock implementation - in production, integrate with actual API
        days_diff = (end_date - start_date).days
        base_price = 10000
        
        prices = []
        for i in range(0, days_diff, 30):  # Monthly prices
            # Simulate price fluctuation
            fluctuation = (i / 30) * 0.01  # 1% increase per month (simplified)
            price = base_price * (1 + fluctuation)
            prices.append(price)
        
        return prices
    
    @staticmethod
    def get_current_price() -> float:
        """Get current gold price"""
        try:
            # Mock API call - replace with actual implementation
            # Example: requests.get('https://api.metalpriceapi.com/v1/latest?api_key=YOUR_KEY&base=USD&symbols=XAU')
            
            # Return mock current price
            return 5850.00
            
        except Exception as e:
            print(f"Error fetching current gold price: {e}")
            return 10500.00  # Fallback price


# Example usage and testing
if __name__ == "__main__":
    calculator = GoldSIPCalculator()
    
    # Example calculation
    results = calculator.calculate_sip_returns(
        monthly_amount=10000,
        duration_months=24,
        average_gold_price=8000,  # Realistic average for 12.5% CAGR
        current_gold_price=10500,
        start_date=datetime.date(2022, 1, 1)
    )
    
    print("=== Gold SIP Calculator Test ===")
    print(calculator.generate_summary_text(results))
    
    # Monthly breakdown example
    breakdown = calculator.calculate_monthly_breakdown(
        monthly_amount=10000,
        duration_months=6,
        start_date=datetime.date(2024, 1, 1)
    )
    
    print("\n=== Monthly Breakdown (First 3 months) ===")
    for month_data in breakdown[:3]:
        print(f"Month {month_data['month']}: Invested {calculator.format_currency(month_data['investment_amount'])}, "
              f"Gold Price: {calculator.format_currency(month_data['gold_price'])}, "
              f"Bought: {calculator.format_weight(month_data['grams_bought'])}")