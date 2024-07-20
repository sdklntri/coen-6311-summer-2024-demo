const express = require('express');
const router = express.Router();

module.exports = function(db) {
    router.get('/', (req, res) => {
        const { email } = req.query;

        db.get("SELECT * FROM subscribers WHERE email = ?", [email], (err, row) => {
            if (err) {
                console.error('Error querying database:', err);
                return res.status(500).json({ message: 'Error querying database' });
            }
            if (!row) {
                return res.status(400).json({ message: 'Email not found' });
            }

            db.run("UPDATE subscribers SET verified = ? WHERE email = ?", [1, email], (err) => {
                if (err) {
                    console.error('Error updating database:', err);
                    return res.status(500).json({ message: 'Error updating database' });
                }

                res.send('Email verified successfully!');
            });
        });
    });

    return router;
};
