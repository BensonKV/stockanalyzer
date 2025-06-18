from flask import Flask, render_template, request, jsonify
from datetime import datetime
import yfinance as yf
import logging
from typing import Dict, Union
import requests

# Initialize Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# app.py

POPULAR_STOCKS = [
    {'ticker': 'AAPL', 'name': 'Apple'},
    {'ticker': 'MSFT', 'name': 'Microsoft'},
    {'ticker': 'GOOGL', 'name': 'Google'},
    {'ticker': 'AMZN', 'name': 'Amazon'},
    {'ticker': 'TSLA', 'name': 'Tesla'},
    {'ticker': 'NVDA', 'name': 'NVIDIA'},
    {'ticker': 'NFLX', 'name': 'Netflix'},
    {'ticker': 'META', 'name': 'Meta'},
    {'ticker': 'INTC', 'name': 'Intel'},
    {'ticker': 'DIS', 'name': 'Walt Disney'},
    {'ticker': 'BA', 'name': 'Boeing'},
    {'ticker': 'PYPL', 'name': 'PayPal'},
    {'ticker': 'AMD', 'name': 'Advanced Micro Devices'},
    {'ticker': 'CSCO', 'name': 'Cisco Systems'},
    {'ticker': 'IBM', 'name': 'IBM'},
    {'ticker': 'V', 'name': 'Visa'},
    {'ticker': 'MA', 'name': 'Mastercard'},
    {'ticker': 'PG', 'name': 'Procter & Gamble'},
    {'ticker': 'KO', 'name': 'Coca-Cola'},
    {'ticker': 'PFE', 'name': 'Pfizer'},
    {'ticker': 'JNJ', 'name': 'Johnson & Johnson'},
    {'ticker': 'WMT', 'name': 'Walmart'},
    {'ticker': 'GS', 'name': 'Goldman Sachs'},
    {'ticker': 'SPGI', 'name': 'S&P Global'},
    {'ticker': 'MCD', 'name': 'McDonald\'s'},
    {'ticker': 'LMT', 'name': 'Lockheed Martin'},
    {'ticker': 'CVX', 'name': 'Chevron'},
    {'ticker': 'XOM', 'name': 'ExxonMobil'},
    {'ticker': 'T', 'name': 'AT&T'},
    {'ticker': 'VZ', 'name': 'Verizon'},
    {'ticker': 'UPS', 'name': 'United Parcel Service'},
    {'ticker': 'AMT', 'name': 'American Tower'},
    {'ticker': 'CL', 'name': 'Colgate-Palmolive'},
    {'ticker': 'WFC', 'name': 'Wells Fargo'},
    {'ticker': 'UNH', 'name': 'UnitedHealth'},
    {'ticker': 'CVS', 'name': 'CVS Health'},
    {'ticker': 'BABA', 'name': 'Alibaba'},
    {'ticker': 'TME', 'name': 'Tencent Music'},
    {'ticker': 'SQ', 'name': 'Square'},
    {'ticker': 'RBLX', 'name': 'Roblox'},
    {'ticker': 'Z', 'name': 'Zillow'},
    {'ticker': 'TWTR', 'name': 'Twitter'},
    {'ticker': 'SPOT', 'name': 'Spotify'},
    {'ticker': 'SNAP', 'name': 'Snapchat'},
    {'ticker': 'EA', 'name': 'Electronic Arts'},
    {'ticker': 'LYFT', 'name': 'Lyft'},
    {'ticker': 'UBER', 'name': 'Uber'},
    {'ticker': 'RKT', 'name': 'Rocket Companies'},
    {'ticker': 'SE', 'name': 'Sea Limited'},
    {'ticker': 'SHOP', 'name': 'Shopify'},
    {'ticker': 'PINS', 'name': 'Pinterest'},
    {'ticker': 'DOCU', 'name': 'DocuSign'},
    {'ticker': 'SQ', 'name': 'Square'},
    {'ticker': 'WORK', 'name': 'Slack Technologies'},
    {'ticker': 'EXPE', 'name': 'Expedia'},
    {'ticker': 'CRM', 'name': 'Salesforce'},

    # Indian Stocks
    {'ticker': 'TCS', 'name': 'Tata Consultancy Services'},
    {'ticker': 'INFY', 'name': 'Infosys'},
    {'ticker': 'RELIANCE', 'name': 'Reliance Industries'},
    {'ticker': 'HDFCBANK', 'name': 'HDFC Bank'},
    {'ticker': 'ICICIBANK', 'name': 'ICICI Bank'},
    {'ticker': 'BHARTIARTL', 'name': 'Bharti Airtel'},
    {'ticker': 'LT', 'name': 'Larsen & Toubro'},
    {'ticker': 'HINDUNILVR', 'name': 'Hindustan Unilever'},
    {'ticker': 'BAJAJFINSV', 'name': 'Bajaj Finserv'},
    {'ticker': 'MARUTI', 'name': 'Maruti Suzuki'},
    {'ticker': 'M&M', 'name': 'Mahindra & Mahindra'},
    {'ticker': 'ASIANPAINT', 'name': 'Asian Paints'},
    {'ticker': 'ULTRACEMCO', 'name': 'UltraTech Cement'},
    {'ticker': 'WIPRO', 'name': 'Wipro'},
    {'ticker': 'SBIN', 'name': 'State Bank of India'},
    {'ticker': 'ITC', 'name': 'ITC Limited'},
    {'ticker': 'TATAMOTORS', 'name': 'Tata Motors'},
    {'ticker': 'POWERGRID', 'name': 'Power Grid Corporation'},
    {'ticker': 'NTPC', 'name': 'NTPC Limited'},
    {'ticker': 'SUNPHARMA', 'name': 'Sun Pharmaceutical Industries'},
    {'ticker': 'BPCL', 'name': 'Bharat Petroleum'},
    {'ticker': 'IOC', 'name': 'Indian Oil Corporation'},
    {'ticker': 'GAIL', 'name': 'GAIL India'},
    {'ticker': 'INDUSINDBK', 'name': 'IndusInd Bank'},
    {'ticker': 'TATAPOWER', 'name': 'Tata Power'},
    {'ticker': 'DIVISLAB', 'name': 'Divi\'s Laboratories'},
    {'ticker': 'DRREDDY', 'name': 'Dr. Reddy\'s Laboratories'},
    {'ticker': 'AUBANK', 'name': 'AU Small Finance Bank'},
    {'ticker': 'HDFCLIFE', 'name': 'HDFC Life Insurance'},
    {'ticker': 'BAJFINANCE', 'name': 'Bajaj Finance'},
    {'ticker': 'NESTLEIND', 'name': 'Nestle India'},
    {'ticker': 'COALINDIA', 'name': 'Coal India'},
    {'ticker': 'ADANIGREEN', 'name': 'Adani Green Energy'},
    {'ticker': 'ADANIPORTS', 'name': 'Adani Ports and SEZ'},
    {'ticker': 'TATACONSUM', 'name': 'Tata Consumer Products'},
    {'ticker': 'HDFCAMC', 'name': 'HDFC Asset Management'},
    {'ticker': 'SHREECEM', 'name': 'Shree Cement'},
    {'ticker': 'TECHM', 'name': 'Tech Mahindra'},
    {'ticker': 'CIPLA', 'name': 'Cipla'},
    # Feel free to add more Indian stocks
]
def get_stock_categories():
    return {
        'technology': [
            {'ticker': 'AAPL', 'name': 'Apple'},
            {'ticker': 'MSFT', 'name': 'Microsoft'},
            {'ticker': 'GOOGL', 'name': 'Google'},
            {'ticker': 'AMZN', 'name': 'Amazon'},
        ],
        'finance': [
            {'ticker': 'JPM', 'name': 'JPMorgan Chase'},
            {'ticker': 'GS', 'name': 'Goldman Sachs'},
            {'ticker': 'WFC', 'name': 'Wells Fargo'},
            {'ticker': 'C', 'name': 'Citigroup'},
        ],
        'consumer_goods': [
            {'ticker': 'KO', 'name': 'Coca-Cola'},
            {'ticker': 'PG', 'name': 'Procter & Gamble'},
            {'ticker': 'PEP', 'name': 'PepsiCo'},
            {'ticker': 'MCD', 'name': 'McDonald\'s'},
        ]
    }



@app.template_filter('datetimeformat')
def datetimeformat(value):
    from datetime import datetime
    return datetime.fromtimestamp(value).strftime('%b %d, %Y %I:%M %p')


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockAnalyzer:
    """Handles all stock data retrieval and processing"""
    
    @staticmethod
    def get_stock_data(ticker: str, period: str = '1y') -> Dict[str, Union[list, str, float]]:
        """Fetch and process stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {ticker}")
            
            # Calculate technical indicators
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean().fillna(0)
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean().fillna(0)
            
            return {
                'success': True,
                'ticker': ticker,
                'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                'prices': hist['Close'].tolist(),
                'sma20': hist['SMA_20'].tolist(),
                'sma50': hist['SMA_50'].tolist(),
                'company': stock.info.get('longName', ticker),
                'current_price': stock.info.get('currentPrice', 0),
                'market_cap': stock.info.get('marketCap', 0),
                'pe_ratio': stock.info.get('trailingPE', 0),
                '52_week_high': stock.info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': stock.info.get('fiftyTwoWeekLow', 0)
            }
        except Exception as e:
            logger.error(f"Error processing {ticker}: {str(e)}")
            return {
                'success': False,
                'error': f"Error processing {ticker}: {str(e)}",
                'ticker': ticker
            }

    @staticmethod
    def get_stock_news(ticker: str) -> list:
        """Fetch recent news articles related to the stock ticker"""
        try:
            api_key = 'd050g0pr01qrsogukg3gd050g0pr01qrsogukg40'
            url = f'https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-01-01&to=2025-01-01&token={api_key}'
            response = requests.get(url)
            response.raise_for_status()
            news = response.json()

            return news[:5]  # return top 5 articles
        except Exception as e:
            logger.error(f"Failed to fetch news for {ticker}: {str(e)}")
            return []

@app.route('/')
def home() -> str:
    """Render the main index page"""
    return render_template('index.html', stocks=get_stock_categories(), now=datetime.now())
    
    # Define stock categories
    stock_categories = {
        'technology': [
            {'ticker': 'AAPL', 'name': 'Apple'},
            {'ticker': 'MSFT', 'name': 'Microsoft'},
            {'ticker': 'GOOGL', 'name': 'Google'},
            {'ticker': 'AMZN', 'name': 'Amazon'},
            # Add more technology stocks
        ],
        'finance': [
            {'ticker': 'JPM', 'name': 'JPMorgan Chase'},
            {'ticker': 'GS', 'name': 'Goldman Sachs'},
            {'ticker': 'WFC', 'name': 'Wells Fargo'},
            {'ticker': 'C', 'name': 'Citigroup'},
            # Add more finance stocks
        ],
        'consumer_goods': [
            {'ticker': 'KO', 'name': 'Coca-Cola'},
            {'ticker': 'PG', 'name': 'Procter & Gamble'},
            {'ticker': 'PEP', 'name': 'PepsiCo'},
            {'ticker': 'MCD', 'name': 'McDonald\'s'},
            # Add more consumer goods stocks
        ],
        
    }
    
    return render_template('index.html', stocks=stock_categories, now=datetime.now())

@app.route('/analyze', methods=['GET'])
def analyze() -> str:
    ticker = request.args.get('ticker', '').strip().upper()
    if not ticker.isalpha() or not (1 <= len(ticker) <= 5):
       return render_template('index.html',
                           error="Invalid stock symbol. Ensure the symbol is 1-5 letters.",
                           now=datetime.now(),
                           stocks=get_stock_categories())

    
    stock_data = StockAnalyzer.get_stock_data(ticker, period='1y')
    if not stock_data['success']:
     return render_template('index.html',
                           error=f"Could not find data for {ticker}. Please try another symbol.",
                           now=datetime.now(),
                           stocks=get_stock_categories())


    stock_news = StockAnalyzer.get_stock_news(ticker)

    return render_template('dashboard.html',
                           ticker=ticker,
                           data=stock_data,
                           news=stock_news)

@app.route('/api/data/<ticker>', methods=['GET'])
def stock_data(ticker: str) -> Dict:
    """API endpoint for stock data"""
    period = request.args.get('period', '1y')
    data = StockAnalyzer.get_stock_data(ticker, period)
    
    if data['success']:
        return jsonify(data), 200
    return jsonify(data), 400

@app.errorhandler(404)
def page_not_found(e) -> str:
    return render_template('404.html', now=datetime.now()), 404

@app.errorhandler(500)
def internal_error(e) -> str:
    logger.error(f"Server error: {str(e)}")
    return render_template('500.html', now=datetime.now()), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

