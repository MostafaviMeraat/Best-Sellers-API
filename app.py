from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def get_bestsellers(category_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(category_url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = []
        # Find best seller items
        for item in soup.select('div[cel_widget_id^="MAIN-SEARCH_RESULTS"]'):
            title_elem = item.select_one('a.a-link-normal span.a-text-normal')
            price_elem = item.select_one('span.a-price span.a-offscreen')
            rank_elem = item.select_one('span.a-size-small.a-color-secondary')
            
            if title_elem:
                items.append({
                    'title': title_elem.get_text(strip=True),
                    'price': price_elem.get_text(strip=True) if price_elem else 'N/A',
                    'rank': rank_elem.get_text(strip=True) if rank_elem else 'N/A'
                })
        
        # Return top 10
        return items[:10]
    
    except Exception as e:
        return {'error': str(e)}

@app.route('/bestsellers', methods=['GET'])
def get_bestsellers_api():
    category = request.args.get('category', 'electronics')
    
    # Amazon Best Sellers categories
    categories = {
        'electronics': 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/',
        'books': 'https://www.amazon.com/Best-Sellers-Books/zgbs/books/',
        'toys': 'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/',
        'kitchen': 'https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/'  # ✅ ADDED
    }
    
    url = categories.get(category, categories['electronics'])
    data = get_bestsellers(url)
    
    return jsonify({
        'category': category,
        'timestamp': time.time(),
        'data': data
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Amazon Best Sellers API',
        'usage': '/bestsellers?category=electronics|books|toys|kitchen'  # Also update this line
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
