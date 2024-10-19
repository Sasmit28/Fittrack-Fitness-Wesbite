from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models import db, User
from config import Config
from routes import main
import joblib
import pandas as pd
import secrets 

app2 = Flask(__name__)
app2.secret_key = secrets.token_hex(16) 
app2.config['SECRET_KEY'] = secrets.token_hex(16)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fittrack.db'  # Use SQLite for simplicity
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app2)

# Load the model and dataset
model = joblib.load('calorie.pkl')

# Assuming this is the cleaned food dataset
data_emoji_foods_cleaned = pd.read_csv('Emoji Diet Nutritional Data (g) - EmojiFoods (g).csv')

# Function to calculate the nutrients based on serving size
def calculate_nutrients(food_item, serving_size, data):
    food_data = data[data['name'].str.lower() == food_item.lower()]

    if food_data.empty:
        return None

    nutrient_data = food_data[['Calories', 'Carbohydrates', 'Total_Fat']]
    scaled_nutrients = nutrient_data * serving_size
    return scaled_nutrients.values.flatten().reshape(1, -1)  # Return as 2D array for prediction



# Register the Blueprint
app2.register_blueprint(main)

@app2.route('/')
def index():
    return render_template('index.html')


@app2.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Here you would typically set up a session for the logged-in user
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app2.route('/home')
def home():
    return render_template('home.html')

@app2.route('/injury-rehabilitation')
def injury_rehabilitation():
    return render_template('injury-rehabilitation.html')

@app2.route('/personalised')
def personalised():
    return render_template('personalised.html')


@app2.route('/plans')
def plans():
    return render_template('plans.html')

@app2.route('/premium')
def premium():
    return render_template('premium.html')

@app2.route('/report-injury')
def report_injury():
    return render_template('report-injury.html')

@app2.route('/subscription')
def subscription():
    return render_template('subscription.html')

@app2.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered", 400
        
        # Create new user
        new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
        
        # Add new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500
        
        # Redirect to home page after successful signup
        return redirect(url_for('home'))
    
    return render_template('signup.html')

@app2.route('/treat-injury')
def treat_injury():
    return render_template('treat-injury.html')

@app2.route('/workout-plans')
def workout_plans():
    return render_template('workout-plans.html')

@app2.route('/diet-plans')
def diet_plans():
    return render_template('diet-plans.html')



# Flask route to handle the prediction request
@app2.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        food_item = data.get('food_item')
        serving_size = 200  # data.get('serving_size')

        if not food_item or not serving_size:
            return jsonify({'error': 'Invalid input.'}), 400

        nutrients = calculate_nutrients(food_item, serving_size, data_emoji_foods_cleaned)
        if nutrients is None:
            return jsonify({'error': f"Food item '{food_item}' not found."}), 404

        # Run prediction
        predicted_nutrients = model.predict(nutrients)
        print(predicted_nutrients)
        # Format the response as rounded values
        response = {
            'protein': round(predicted_nutrients[0][0]),
            'carbs': round(predicted_nutrients[0][1]),
            'fat': round(predicted_nutrients[0][2]),
            'calories': round(predicted_nutrients[0][3])
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app2.run(host="127.0.0.1", port=5500, debug=True)