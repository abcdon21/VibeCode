
# handles the complete flask project
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import base64
import io
from datetime import datetime, timedelta
import re
import json
import random

# create an instance for calling flask functions
app = Flask(__name__)  # this defines that this is our main page
app.secret_key = 'your-secret-key-here'  # needed for flash messages

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Food database with expiry predictions
FOOD_DATABASE = {
    'fruits': {
        'apple': {'shelf_life': 7, 'spoilage_signs': ['dark spots', 'soft texture']},
        'banana': {'shelf_life': 5, 'spoilage_signs': ['brown spots', 'soft']},
        'orange': {'shelf_life': 10, 'spoilage_signs': ['mold', 'soft spots']},
        'strawberry': {'shelf_life': 3, 'spoilage_signs': ['mold', 'mushy']},
        'grapes': {'shelf_life': 5, 'spoilage_signs': ['wrinkled', 'soft']},
    },
    'vegetables': {
        'tomato': {'shelf_life': 6, 'spoilage_signs': ['soft spots', 'wrinkled']},
        'carrot': {'shelf_life': 14, 'spoilage_signs': ['soft', 'white spots']},
        'lettuce': {'shelf_life': 4, 'spoilage_signs': ['wilted', 'brown edges']},
        'potato': {'shelf_life': 21, 'spoilage_signs': ['green color', 'sprouts']},
    },
    'dairy': {
        'milk': {'shelf_life': 5, 'spoilage_signs': ['sour smell', 'chunky']},
        'cheese': {'shelf_life': 10, 'spoilage_signs': ['mold', 'hard texture']},
        'yogurt': {'shelf_life': 7, 'spoilage_signs': ['separation', 'mold']},
    }
}
# create route for webpages
@app.route('/')# this is the home page
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Simple validation
        if name and email and subject and message:
            # In a real app, you would send the email or save to database
            flash(f'Thank you {name}! Your message has been received. We\'ll get back to you soon.', 'success')
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Simple demo authentication (in real app, check against database)
        if email and password:
            # For demo purposes, any email/password combination works
            flash('Login successful! Welcome to your FoodSaver dashboard.', 'success')
            return render_template('login.html')
        else:
            flash('Please enter both email and password.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('login.html')  # Since login.html contains the dashboard

# AI Food Recognition Routes
@app.route('/analyze_food', methods=['POST'])
def analyze_food():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        # Simulate AI analysis (in real app, this would use actual ML models)
        analysis_result = simulate_food_analysis(image_data)
        
        return jsonify({
            'success': True,
            'result': analysis_result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def simulate_food_analysis(image_data):
    """Simulate AI food recognition and OCR analysis"""
    # Random food selection for demo
    food_categories = list(FOOD_DATABASE.keys())
    selected_category = random.choice(food_categories)
    foods_in_category = list(FOOD_DATABASE[selected_category].keys())
    detected_food = random.choice(foods_in_category)
    
    food_info = FOOD_DATABASE[selected_category][detected_food]
    
    # Simulate expiry prediction
    current_date = datetime.now()
    predicted_expiry = current_date + timedelta(days=food_info['shelf_life'])
    
    # Simulate manufacturing date (for packaged items)
    if selected_category in ['dairy']:
        mfg_date = current_date - timedelta(days=random.randint(1, 3))
        expiry_date = mfg_date + timedelta(days=food_info['shelf_life'])
    else:
        mfg_date = None
        expiry_date = predicted_expiry
    
    # Random Forest-like prediction simulation
    urgency_score = predict_expiry_urgency(detected_food, selected_category)
    
    return {
        'food_name': detected_food.title(),
        'category': selected_category.title(),
        'confidence': random.randint(85, 98),
        'shelf_life_days': food_info['shelf_life'],
        'predicted_expiry': expiry_date.strftime('%Y-%m-%d'),
        'mfg_date': mfg_date.strftime('%Y-%m-%d') if mfg_date else None,
        'spoilage_signs': food_info['spoilage_signs'],
        'urgency_score': urgency_score,
        'recommendation': get_recommendation(urgency_score)
    }

def predict_expiry_urgency(food_name, category):
    """Simulate Random Forest classification for expiry prediction"""
    # Features simulation: freshness, storage, temperature, etc.
    features = [
        random.uniform(0.7, 1.0),  # freshness_score
        random.uniform(0.6, 1.0),  # storage_quality
        random.uniform(0.5, 1.0),  # temperature_stability
        len(food_name) / 10,       # food_type_factor
    ]
    
    # Simulate Random Forest decision
    weights = [0.4, 0.3, 0.2, 0.1]
    urgency_score = sum(f * w for f, w in zip(features, weights))
    
    # Convert to 1-10 scale (10 = most urgent)
    return round((1 - urgency_score) * 10, 1)

def get_recommendation(urgency_score):
    """Get recommendation based on urgency score"""
    if urgency_score >= 8:
        return "⚠️ Use immediately or donate today!"
    elif urgency_score >= 6:
        return "🟡 Use within 1-2 days"
    elif urgency_score >= 4:
        return "🟢 Use within this week"
    else:
        return "✅ Fresh - can store for several days"

@app.route('/get_expiry_predictions')
def get_expiry_predictions():
    """Get Random Forest predictions for all stored items"""
    # Simulate stored food items
    stored_items = [
        {'name': 'Milk', 'category': 'dairy', 'stored_date': '2025-11-28'},
        {'name': 'Banana', 'category': 'fruits', 'stored_date': '2025-11-29'},
        {'name': 'Tomato', 'category': 'vegetables', 'stored_date': '2025-11-27'},
        {'name': 'Apple', 'category': 'fruits', 'stored_date': '2025-11-26'},
    ]
    
    predictions = []
    for item in stored_items:
        urgency = predict_expiry_urgency(item['name'], item['category'])
        predictions.append({
            'name': item['name'],
            'urgency_score': urgency,
            'recommendation': get_recommendation(urgency),
            'stored_date': item['stored_date']
        })
    
    # Sort by urgency (highest first)
    predictions.sort(key=lambda x: x['urgency_score'], reverse=True)
    
    return jsonify({
        'success': True,
        'predictions': predictions
    })

# to run the application in local debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5001)