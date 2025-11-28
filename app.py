
# handles the complete flask project
from flask import Flask, render_template, request, redirect, url_for, flash
# create an instance for calling flask functions
app = Flask(__name__)  # this defines that this is our main page
app.secret_key = 'your-secret-key-here'  # needed for flash messages
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

# to run the application in local debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5001)