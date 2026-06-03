const config = require('../config');

const authMiddleware = (req, res, next) => {
    const token = req.headers['authorization'];
    if (token === config.adminToken) {
        next();
    } else {
        res.status(401).json({ error: "Unauthorized" });
    }
};

module.exports = authMiddleware;
