const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const verifyRoutes = require('./email-verification/routes/verify');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const db = new sqlite3.Database(':memory:');

// Create table
db.serialize(() => {
    db.run("CREATE TABLE subscribers (email TEXT PRIMARY KEY, verified INTEGER)");
});

// Nodemailer setup
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'your-email@gmail.com',
        pass: 'your-email-password'
    }
});

// Route for subscription
app.post('/subscribe', (req, res) => {
    const { email } = req.body;
    const verificationLink = `http://localhost:3000/verify?email=${encodeURIComponent(email)}`;

    const mailOptions = {
        from: 'your-email@gmail.com',
        to: email,
        subject: 'Email Verification',
        text: `Please verify your email by clicking on the following link: ${verificationLink}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error('Error sending verification email:', error);
            return res.status(500).json({ message: 'Error sending verification email' });
        }
        console.log('Email sent:', info.response);

        // Insert email into the SQLite database with verified: false
        db.run("INSERT INTO subscribers (email, verified) VALUES (?, ?)", [email, 0], (err) => {
            if (err) {
                console.error('Error saving email to database:', err);
                return res.status(500).json({ message: 'Error saving email to database' });
            }
            res.status(200).json({ message: 'Verification email sent' });
        });
    });
});

// Use the verify routes
app.use('/verify', verifyRoutes(db));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
