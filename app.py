from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

# YOUR API KEY FROM OMKAR
API_KEY = "ok_48532137cc246567d29f576ee198e1cb"

def get_bestsellers_omkar(category):
    """Get real Amazon bestsellers using Omkar API"""
    try:
        # Omkar API endpoint for Amazon bestsellers
        url = f"https://api.omkar.cloud/amazon/bestsellers/"
        
        headers = {
            "API-Key": API_KEY  # Important: header name is 'API-Key'
        }
        
        params = {
            "category": category
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Extract the product data
            if data.get('status') == 'success':
                products = data.get('data', [])
                return products[:10]  # Return top 10
            else:
                return get_mock_data(category)
        else:
            return get_mock_data(category)
            
    except Exception as e:
        print(f"Error: {e}")
        return get_mock_data(category)

def get_mock_data(category):
    """Fallback mock data if API fails"""
    mock_data = {
        'kitchen': [
            {'title': 'KitchenAid Stand Mixer', 'price': '$329.99', 'rating': '4.8', 'rank': '1'},
            {'title': 'Instant Pot Duo', 'price': '$89.99', 'rating': '4.7', 'rank': '2'},
            {'title': 'Cuisinart Knife Set', 'price': '$129.99', 'rating': '4.6', 'rank': '3'},
            {'title': 'Ninja Blender', 'price': '$89.99', 'rating': '4.5', 'rank': '4'},
            {'title': 'Oxo Good Grips', 'price': '$24.99', 'rating': '4.4', 'rank': '5'},
        ],
        'electronics': [
            {'title': 'Apple AirPods Pro', 'price': '$249.99', 'rating': '4.7', 'rank': '1'},
            {'title': 'Samsung Galaxy S24', 'price': '$799.99', 'rating': '4.5', 'rank': '2'},
            {'title': 'Sony WH-1000XM5', 'price': '$399.99', 'rating': '4.6', 'rank': '3'},
            {'title': 'Apple Watch Series 9', 'price': '$399.99', 'rating': '4.5', 'rank': '4'},
            {'title': 'Dyson V15 Vacuum', 'price': '$699.99', 'rating': '4.4', 'rank': '5'},
        ],
        'books': [
            {'title': 'The Covenant of Water', 'price': '$18.99', 'rating': '4.5', 'rank': '1'},
            {'title': 'Atomic Habits', 'price': '$14.99', 'rating': '4.8', 'rank': '2'},
            {'title': 'Fourth Wing', 'price': '$16.99', 'rating': '4.7', 'rank': '3'},
            {'title': 'The Women', 'price': '$19.99', 'rating': '4.6', 'rank': '4'},
            {'title': 'James', 'price': '$17.99', 'rating': '4.5', 'rank': '5'},
        ],
        'toys': [
            {'title': 'Lego Creator Set', 'price': '$49.99', 'rating': '4.9', 'rank': '1'},
            {'title': 'Barbie Dreamhouse', 'price': '$199.99', 'rating': '4.6', 'rank': '2'},
            {'title': 'Hot Wheels Track', 'price': '$39.99', 'rating': '4.7', 'rank': '3'},
            {'title': 'Nerf Gun', 'price': '$29.99', 'rating': '4.5', 'rank': '4'},
            {'title': 'Play-Doh Set', 'price': '$19.99', 'rating': '4.4', 'rank': '5'},
        ]
    }
    return mock_data.get(category, mock_data['electronics'])

@app.route('/bestsellers', methods=['GET'])
def get_bestsellers_api():
    category = request.args.get('category', 'electronics').lower()
    
    # Try to get real data from Omkar
    data = get_bestsellers_omkar(category)
    
    return jsonify({
        'category': category,
        'timestamp': time.time(),
        'data': data,
        'source': 'Omkar API (real data)' if data and data != get_mock_data(category) else 'Mock Data (fallback)',
        'status': 'success'
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Amazon Best Sellers API - REAL DATA from Omkar',
        'usage': '/bestsellers?category=kitchen|electronics|books|toys',
        'categories': ['kitchen', 'electronics', 'books', 'toys'],
        'status': 'online'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
