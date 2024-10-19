from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection
def connect_db():
    conn = psycopg2.connect(
        dbname="gym_db", user="postgres", password="root", host="localhost", port="5432"
    )
    return conn

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Save data into the database
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                        (name, email, password))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('home'))
        except Exception as e:
            return f"An error occurred: {e}"
    
    return render_template('signup.html')  # This should render the form template

# @app.route('/home')
# def home():
#     return "Welcome to FitTrack"

if __name__ == '__main__':
    app.run(debug=True)
