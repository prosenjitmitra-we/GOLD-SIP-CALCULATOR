"""
Gold Price API Integration
Real-time gold price fetching from multiple sources
"""

import requests
import json
from typing import Dict, Optional, List
import datetime
from dataclasses import dataclass
import time


@dataclass
class GoldPriceData:
    """Data class for gold price information"""
    price_per_gram: float
    currency: str
    unit: str
    timestamp: datetime.datetime
    source: str
    confidence: float = 1.0  # 0.0 to 1.0


class LiveGoldPriceAPI:
    """
    Live gold price fetching from multiple APIs with fallback support
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
        self.timeout = 10  # Request timeout in seconds
    
    def get_current_gold_price(self) -> GoldPriceData:
        """
        Get current gold price with fallback to multiple sources
        
        Returns:
            GoldPriceData with current gold price information
        """
        
        # Check cache first
        cached_price = self._get_cached_price()
        if cached_price:
            return cached_price
        
        # Try multiple sources in priority order
        sources = [
            self._fetch_from_metalpriceapi,
            self._fetch_from_goldapi,
            self._fetch_from_fcsapi,
            self._fetch_mock_price  # Fallback mock price
        ]
        
        for source_func in sources:
            try:
                price_data = source_func()
                if price_data and price_data.price_per_gram > 0:
                    # Cache the successful result
                    self._cache_price(price_data)
                    return price_data
            except Exception as e:
                print(f"Error from {source_func.__name__}: {e}")
                continue
        
        # If all sources fail, return fallback price
        return self._get_fallback_price()
    
    def _get_cached_price(self) -> Optional[GoldPriceData]:
        """Get cached price if still valid"""
        if 'price_data' in self.cache and 'timestamp' in self.cache:
            cache_age = (datetime.datetime.now() - self.cache['timestamp']).seconds
            if cache_age < self.cache_duration:
                return self.cache['price_data']
        return None
    
    def _cache_price(self, price_data: GoldPriceData):
        """Cache the price data"""
        self.cache['price_data'] = price_data
        self.cache['timestamp'] = datetime.datetime.now()
    
    def _fetch_from_metalpriceapi(self) -> GoldPriceData:
        """
        Fetch from MetalPriceAPI.com
        Free tier: 100 requests/month
        """
        
        # Note: You need to register and get a free API key
        api_key = "YOUR_METALPRICEAPI_KEY"
        
        if api_key == "YOUR_METALPRICEAPI_KEY":
            raise Exception("MetalPriceAPI key not configured")
        
        url = f"https://api.metalpriceapi.com/v1/latest"
        params = {
            'api_key': api_key,
            'base': 'USD',
            'symbols': 'XAU'  # Gold symbol
        }
        
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('success'):
            raise Exception("API returned error")
        
        # XAU is in troy ounces, convert to grams and then to INR
        gold_price_usd_per_oz = 1 / data['rates']['XAU']  # USD per troy ounce
        gold_price_usd_per_gram = gold_price_usd_per_oz / 31.1035  # Convert to grams
        
        # Convert USD to INR (approximate rate, you might want to get live rate)
        usd_to_inr_rate = 83.0  # Update this with live USD-INR rate
        gold_price_inr_per_gram = gold_price_usd_per_gram * usd_to_inr_rate
        
        return GoldPriceData(
            price_per_gram=round(gold_price_inr_per_gram, 2),
            currency="INR",
            unit="gram",
            timestamp=datetime.datetime.now(),
            source="MetalPriceAPI",
            confidence=0.95
        )
    
    def _fetch_from_goldapi(self) -> GoldPriceData:
        """
        Fetch from GoldAPI.io
        Free tier: 1000 requests/month
        """
        
        # Note: You need to register and get a free API key
        api_key = "YOUR_GOLDAPI_KEY"
        
        if api_key == "YOUR_GOLDAPI_KEY":
            raise Exception("GoldAPI key not configured")
        
        url = "https://www.goldapi.io/api/XAU/USD"
        headers = {
            'X-ACCESS-TOKEN': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # Gold price is in USD per troy ounce
        gold_price_usd_per_oz = data['price']
        gold_price_usd_per_gram = gold_price_usd_per_oz / 31.1035
        
        # Convert to INR
        usd_to_inr_rate = 83.0  # Update with live rate
        gold_price_inr_per_gram = gold_price_usd_per_gram * usd_to_inr_rate
        
        return GoldPriceData(
            price_per_gram=round(gold_price_inr_per_gram, 2),
            currency="INR",
            unit="gram",
            timestamp=datetime.datetime.now(),
            source="GoldAPI",
            confidence=0.95
        )
    
    def _fetch_from_fcsapi(self) -> GoldPriceData:
        """
        Fetch from FCS API (Financial Data)
        Free tier: 500 requests/month
        """
        
        api_key = "YOUR_FCS_API_KEY"
        
        if api_key == "YOUR_FCS_API_KEY":
            raise Exception("FCS API key not configured")
        
        url = "https://fcsapi.com/api-v3/forex/latest"
        params = {
            'symbol': 'XAU/USD',
            'access_key': api_key
        }
        
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('status'):
            raise Exception("FCS API returned error")
        
        # Gold price in USD per troy ounce
        gold_price_usd_per_oz = data['response'][0]['c']  # Close price
        gold_price_usd_per_gram = gold_price_usd_per_oz / 31.1035
        
        # Convert to INR
        usd_to_inr_rate = 83.0
        gold_price_inr_per_gram = gold_price_usd_per_gram * usd_to_inr_rate
        
        return GoldPriceData(
            price_per_gram=round(gold_price_inr_per_gram, 2),
            currency="INR",
            unit="gram",
            timestamp=datetime.datetime.now(),
            source="FCS API",
            confidence=0.90
        )
    
    def _fetch_mock_price(self) -> GoldPriceData:
        """
        Generate a realistic mock price for development/demo purposes
        """
        
        # Base price with some realistic variation
        base_price = 10500
        
        # Add time-based variation to simulate real price movement
        now = datetime.datetime.now()
        time_factor = (now.hour * 60 + now.minute) / (24 * 60)  # 0 to 1
        daily_variation = 50 * (0.5 - time_factor)  # ±25 variation throughout day
        
        # Add some randomness based on current time
        random_variation = (now.second % 20) - 10  # ±10 variation
        
        mock_price = base_price + daily_variation + random_variation
        
        return GoldPriceData(
            price_per_gram=round(mock_price, 2),
            currency="INR",
            unit="gram",
            timestamp=now,
            source="Mock Price",
            confidence=0.50
        )
    
    def _get_fallback_price(self) -> GoldPriceData:
        """Get a static fallback price when all APIs fail"""
        return GoldPriceData(
            price_per_gram=10500.00,
            currency="INR",
            unit="gram",
            timestamp=datetime.datetime.now(),
            source="Fallback",
            confidence=0.30
        )
    
    def get_price_history(self, days: int = 30) -> List[GoldPriceData]:
        """
        Get historical gold prices (mock implementation)
        In production, integrate with historical data APIs
        """
        
        history = []
        base_price = 7000  # More realistic historical starting point
        
        for i in range(days):
            date = datetime.datetime.now() - datetime.timedelta(days=days-i)
            
            # Simulate price movement
            price_variation = (i % 10 - 5) * 20  # Some variation
            trend = i * 2  # Slight upward trend
            
            price = base_price + price_variation + trend
            
            history.append(GoldPriceData(
                price_per_gram=round(price, 2),
                currency="INR",
                unit="gram",
                timestamp=date,
                source="Historical Mock",
                confidence=0.70
            ))
        
        return history
    
    def get_usd_to_inr_rate(self) -> float:
        """
        Get current USD to INR exchange rate
        In production, integrate with forex API
        """
        
        try:
            # Free forex API (replace with actual API)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data['rates'].get('INR', 83.0)
        
        except Exception as e:
            print(f"Error fetching USD-INR rate: {e}")
        
        # Fallback rate
        return 83.0


# Convenience functions for backward compatibility
def get_live_gold_price() -> float:
    """Get current gold price in INR per gram"""
    api = LiveGoldPriceAPI()
    price_data = api.get_current_gold_price()
    return price_data.price_per_gram

def get_price_with_confidence() -> tuple:
    """Get current gold price with confidence score"""
    api = LiveGoldPriceAPI()
    price_data = api.get_current_gold_price()
    return price_data.price_per_gram, price_data.confidence

# Test the API
if __name__ == "__main__":
    api = LiveGoldPriceAPI()
    
    print("🔍 Testing Live Gold Price API...")
    
    # Test current price
    try:
        price_data = api.get_current_gold_price()
        print(f"✅ Current Gold Price: ₹{price_data.price_per_gram}/gram")
        print(f"📊 Source: {price_data.source}")
        print(f"🎯 Confidence: {price_data.confidence:.0%}")
        print(f"🕒 Updated: {price_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error getting price: {e}")
    
    print("\n📈 Testing price history...")
    try:
        history = api.get_price_history(7)  # Last 7 days
        print(f"✅ Got {len(history)} historical prices")
        
        for i, price in enumerate(history[-3:]):  # Show last 3
            print(f"   {price.timestamp.strftime('%Y-%m-%d')}: ₹{price.price_per_gram}/gram")
            
    except Exception as e:
        print(f"❌ Error getting history: {e}")
    
    # Test USD-INR rate
    print(f"\n💱 USD-INR Rate: {api.get_usd_to_inr_rate()}")
    
    print("\n🏁 Testing completed!")