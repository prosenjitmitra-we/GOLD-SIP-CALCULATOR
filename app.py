"""
Gold SIP Calculator - Flask Web Application
A chatbot interface for calculating Gold SIP returns
"""

from flask import Flask, render_template, request, jsonify, session
import datetime
import sys
import os

# Add src directory to path to import our calculator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from gold_sip_calculator import GoldSIPCalculator, GoldPriceAPI

app = Flask(__name__)
app.secret_key = 'gold_sip_secret_key_2024'  # Change this in production

# Initialize calculator
calculator = GoldSIPCalculator()

# Conversation states
class ConversationState:
    WELCOME = "welcome"
    ASKING_AMOUNT = "asking_amount"
    ASKING_DURATION = "asking_duration"
    ASKING_AVG_PRICE = "asking_avg_price"
    ASKING_CURRENT_PRICE = "asking_current_price"
    SHOWING_RESULTS = "showing_results"
    COMPLETED = "completed"

@app.route('/')
def index():
    """Main page with chatbot interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '').strip()
    
    # Initialize session state if not exists
    if 'state' not in session:
        session['state'] = ConversationState.WELCOME
        session['data'] = {}
    
    state = session['state']
    data = session['data']
    
    response = process_chat_message(user_message, state, data)
    
    return jsonify(response)

def process_chat_message(user_message, state, data):
    """Process user message based on current conversation state"""
    
    if state == ConversationState.WELCOME:
        # Welcome message
        session['state'] = ConversationState.ASKING_AMOUNT
        return {
            'message': """
🙏 Welcome to Gold SIP Calculator! 

I'll help you calculate your Gold SIP investment returns. Let's get started!

💰 Please enter your **monthly SIP amount** in INR (e.g., 5000, 10000):
            """.strip(),
            'type': 'bot'
        }
    
    elif state == ConversationState.ASKING_AMOUNT:
        # Parse monthly amount
        try:
            amount = float(user_message.replace(',', '').replace('₹', ''))
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            data['monthly_amount'] = amount
            session['state'] = ConversationState.ASKING_DURATION
            session['data'] = data
            
            return {
                'message': f"""
Great! Monthly SIP amount: ₹{amount:,.2f}

📅 Now, please enter the **investment duration** in months (e.g., 12, 24, 36):
                """.strip(),
                'type': 'bot'
            }
        except ValueError:
            return {
                'message': "❌ Please enter a valid amount in numbers only (e.g., 5000, 10000)",
                'type': 'bot'
            }
    
    elif state == ConversationState.ASKING_DURATION:
        # Parse duration
        try:
            duration = int(user_message)
            if duration <= 0:
                raise ValueError("Duration must be positive")
            
            data['duration_months'] = duration
            session['state'] = ConversationState.ASKING_AVG_PRICE
            session['data'] = data
            
            return {
                'message': f"""
Perfect! Duration: {duration} months

📊 Please enter the **average gold price** during your investment period in INR per gram.

📈 For realistic returns (Gold has 12.5% historical CAGR):
• Recent SIP (1-2 years): Use ₹9,000-9,500/gram
• Medium-term (2-3 years): Use ₹7,500-8,500/gram
• Long-term (5+ years): Use ₹5,000-7,000/gram
• Current price: ₹{calculator.get_live_gold_price():.2f}/gram

Enter average gold price per gram:
                """.strip(),
                'type': 'bot'
            }
        except ValueError:
            return {
                'message': "❌ Please enter a valid number of months (e.g., 12, 24, 36)",
                'type': 'bot'
            }
    
    elif state == ConversationState.ASKING_AVG_PRICE:
        # Parse average gold price
        try:
            avg_price = float(user_message.replace(',', '').replace('₹', ''))
            if avg_price <= 0:
                raise ValueError("Price must be positive")
            
            data['average_gold_price'] = avg_price
            session['state'] = ConversationState.ASKING_CURRENT_PRICE
            session['data'] = data
            
            live_price = calculator.get_live_gold_price()
            
            return {
                'message': f"""
Noted! Average gold price: ₹{avg_price:,.2f}/gram

💎 Finally, please enter the **current gold price** per gram in INR.

Live gold price: ₹{live_price:.2f}/gram (You can use this or enter your own)

Enter current gold price per gram:
                """.strip(),
                'type': 'bot'
            }
        except ValueError:
            return {
                'message': "❌ Please enter a valid gold price (e.g., 7000, 8000, 9000)",
                'type': 'bot'
            }
    
    elif state == ConversationState.ASKING_CURRENT_PRICE:
        # Parse current gold price and calculate results
        try:
            current_price = float(user_message.replace(',', '').replace('₹', ''))
            if current_price <= 0:
                raise ValueError("Price must be positive")
            
            data['current_gold_price'] = current_price
            
            # Calculate SIP returns
            results = calculator.calculate_sip_returns(
                monthly_amount=data['monthly_amount'],
                duration_months=data['duration_months'],
                average_gold_price=data['average_gold_price'],
                current_gold_price=data['current_gold_price']
            )
            
            # Store results in session
            session['data']['results'] = results
            session['state'] = ConversationState.SHOWING_RESULTS
            
            summary = calculator.generate_summary_text(results)
            
            return {
                'message': summary + "\n\n" + """
🔄 Would you like to:
• Calculate for different values (type 'new')
• See monthly breakdown (type 'breakdown')
• Get investment tips (type 'tips')

Or just say 'thanks' to end our conversation!
                """.strip(),
                'type': 'bot',
                'results': results
            }
        except ValueError:
            return {
                'message': "❌ Please enter a valid current gold price (e.g., 10200, 10500)",
                'type': 'bot'
            }
    
    elif state == ConversationState.SHOWING_RESULTS:
        # Handle post-calculation options
        user_input = user_message.lower()
        
        if user_input in ['new', 'calculate', 'restart']:
            # Reset for new calculation
            session['state'] = ConversationState.ASKING_AMOUNT
            session['data'] = {}
            
            return {
                'message': """
🔄 Let's calculate a new Gold SIP investment!

💰 Please enter your **monthly SIP amount** in INR (e.g., 5000, 10000):
                """.strip(),
                'type': 'bot'
            }
        
        elif user_input in ['breakdown', 'monthly', 'details']:
            # Show monthly breakdown
            if 'results' in data:
                breakdown = calculator.calculate_monthly_breakdown(
                    monthly_amount=data['monthly_amount'],
                    duration_months=min(data['duration_months'], 12),  # Limit to 12 months for display
                    start_date=datetime.date.today() - datetime.timedelta(days=data['duration_months']*30)
                )
                
                breakdown_text = "📊 **Monthly Investment Breakdown** (Sample)\n\n"
                for i, month_data in enumerate(breakdown[:6]):  # Show first 6 months
                    breakdown_text += f"**Month {month_data['month']}:** Invested ₹{month_data['investment_amount']:,.0f}, Gold Price: ₹{month_data['gold_price']:,.0f}/gram, Bought: {month_data['grams_bought']:.3f}g\n"
                
                if len(breakdown) > 6:
                    breakdown_text += f"... (and {len(breakdown) - 6} more months)\n"
                
                breakdown_text += "\n🔄 Type 'new' for a new calculation or 'thanks' to end!"
                
                return {
                    'message': breakdown_text,
                    'type': 'bot'
                }
        
        elif user_input in ['tips', 'advice', 'help']:
            # Investment tips
            return {
                'message': """
💡 **Gold SIP Investment Tips:**

✅ **Best Practices:**
• Invest consistently every month regardless of gold price
• Gold is a long-term investment (3+ years recommended)
• Don't invest more than 10-15% of portfolio in gold
• Consider Digital Gold for easy SIP investments

⚠️ **Things to Remember:**
• Gold doesn't give dividends or interest
• Price can be volatile in short term
• GST and making charges apply on physical gold
• Digital gold has lower costs and better liquidity

📈 **When to Invest:**
• Market uncertainty periods
• High inflation scenarios
• Portfolio diversification
• Wedding/festival planning

🔄 Type 'new' for another calculation or 'thanks' to end!
                """.strip(),
                'type': 'bot'
            }
        
        elif user_input in ['thanks', 'thank you', 'bye', 'goodbye']:
            session['state'] = ConversationState.COMPLETED
            return {
                'message': """
🙏 Thank you for using the Gold SIP Calculator! 

✨ Remember:
• Gold is a great portfolio diversifier
• Consistent investing beats timing the market
• Stay invested for the long term

Feel free to refresh the page to calculate again anytime! 💛
                """.strip(),
                'type': 'bot'
            }
        
        else:
            return {
                'message': """
I didn't understand that. You can:
• Type 'new' for a new calculation
• Type 'breakdown' for monthly details
• Type 'tips' for investment advice
• Type 'thanks' to end our conversation
                """.strip(),
                'type': 'bot'
            }
    
    else:
        # Default response
        return {
            'message': "Hi! Please refresh the page to start a new Gold SIP calculation. 😊",
            'type': 'bot'
        }

@app.route('/api/gold-price')
def get_gold_price():
    """API endpoint to get current gold price"""
    try:
        price = calculator.get_live_gold_price()
        return jsonify({
            'success': True,
            'price': price,
            'currency': 'INR',
            'unit': 'gram',
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/reset-session')
def reset_session():
    """Reset chat session"""
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)