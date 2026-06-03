const express = require('express');
const config = require('./config');
const db = require('./database/connection');
const routes = require('./routes');

const app = express();
app.use(express.json());

// Routes
app.use('/api', routes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something broke!', success: false });
});

// Initialize DB and start server
db.init().then(() => {
    app.listen(config.port, () => {
        console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
    });
}).catch(err => {
    console.error('Failed to initialize database:', err);
});

module.exports = app;
