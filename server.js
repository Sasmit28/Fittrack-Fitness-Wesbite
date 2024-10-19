const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const path = require('path');
const app = express();
const port = 5500;

// Enable CORS for all routes
app.use(cors());

// Parse JSON bodies and URL-encoded bodies
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Database connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'postgres',
    password: 'root',
    database: 'fittrack'
});

// Connect to the database
db.connect((err) => {
    if (err) {
        console.error('Error connecting to the database:', err);
        return;
    }
    console.log('Connected to the database');
});

// Route for the home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route for the login page
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Route for the signup page
app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

// Route for the main home page after login
app.get('/home', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

// Handle login POST request
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    console.log('Login attempt:', { email, password });
    // TODO: Implement actual login logic here
    // For now, we'll just redirect to the home page
    res.redirect('/home');
});

// Handle signup POST request
app.post('/signup', (req, res) => {
    const { name, email, password } = req.body;
    console.log('Signup attempt:', { name, email, password });
    // TODO: Implement actual signup logic here
    // For now, we'll just redirect to the login page
    res.redirect('/login');
});

// API to handle injury report
app.post('/report-injury', (req, res) => {
    const { injury_name, description } = req.body;

    // Fetch rehabilitation plan from the database based on injury_name
    const query = 'SELECT * FROM rehab_plans WHERE injury_name = ?';
    
    db.query(query, [injury_name], (error, results) => {
        if (error) {
            console.error('Error fetching rehab data:', error);
            return res.status(500).json({ message: 'Database query error' });
        }

        if (results.length === 0) {
            return res.status(404).json({ message: 'No rehabilitation plan found for this injury' });
        }

        const rehabData = results[0];

        res.json({
            message: 'Injury report received',
            injury: {
                name: injury_name,
                description,
                reportedAt: new Date().toISOString(),
            },
            grade: rehabData.grade,
            rehab_steps: JSON.parse(rehabData.rehab_steps),
            diet_recommendation: rehabData.diet_recommendation,
            exercise_images: JSON.parse(rehabData.exercise_images),
            message: rehabData.message
        });
    });
});

// Catch-all route for any unmatched routes
app.get('*', (req, res) => {
    res.status(404).sendFile(path.join(__dirname, 'public', '404.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});