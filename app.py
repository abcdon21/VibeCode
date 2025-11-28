
# handles the complete flask project
from flask import Flask, render_template
# create an instance for calling flask functions
app= Flask(__name__)# this defines that this is our main page
# create route for webpages
@app.route('/')# this is the home page
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')  
def contact():
    return render_template('contact.html')
# # to run the application in local debug mode
if __name__== '__main__':
    app.run()