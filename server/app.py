# app.py
from flask import Flask
from db import db  # Make sure you're importing the db instance correctly
from flask_migrate import Migrate
from routes import api  # Importing the API instance from routes

# Initialize the Flask application
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Using SQLite for this example
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables modification tracking
app.json.compact = False  # Pretty-print JSON responses

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Register the API routes
api.init_app(app)  # Register all routes defined in routes.py

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
