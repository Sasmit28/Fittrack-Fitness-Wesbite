from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from routes import main
import joblib
import pandas as pd
import secrets 

app2 = Flask(__name__)
app2.secret_key = secrets.token_hex(16) 
app2.config['SECRET_KEY'] = secrets.token_hex(16)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fittrack.db'
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app2)

# Load the model and dataset
model = joblib.load('calorie.pkl')
data_emoji_foods_cleaned = pd.read_csv('Emoji Diet Nutritional Data (g) - EmojiFoods (g).csv')

def calculate_nutrients(food_item, serving_size, data):
    food_data = data[data['name'].str.lower() == food_item.lower()]
    if food_data.empty:
        return None
    nutrient_data = food_data[['Calories', 'Carbohydrates', 'Total_Fat']]
    scaled_nutrients = nutrient_data * serving_size
    return scaled_nutrients.values.flatten().reshape(1, -1)

# Register the Blueprint
app2.register_blueprint(main)

@app2.route('/')
def index():
    return render_template('index.html')

@app2.route('/home-web')
def home():
    return render_template('home.html')

@app2.route('/injury-rehabilitation')
def injury_rehabilitation():
    return render_template('injury-rehabilitation.html')

@app2.route('/personalised')
def personalised():
    return render_template('personalised.html')

@app2.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

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
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('signup'))
    
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

@app2.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        food_item = data.get('food_item')
        serving_size = data.get('serving_size', 200)  # Default to 200 if not provided

        if not food_item:
            return jsonify({'error': 'Invalid input. Food item is required.'}), 400

        nutrients = calculate_nutrients(food_item, serving_size, data_emoji_foods_cleaned)
        if nutrients is None:
            return jsonify({'error': f"Food item '{food_item}' not found."}), 404

        predicted_nutrients = model.predict(nutrients)
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
    with app2.app_context():
        db.create_all()  # Create database tables
    app2.run(host="127.0.0.1", port=5500, debug=True)