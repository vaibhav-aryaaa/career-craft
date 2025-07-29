from flask import Flask

# Create an instance of the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, Career Coach!"