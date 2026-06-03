const express = require('express');
const router = express.Router();
const checkoutController = require('../controllers/checkoutController');
const adminController = require('../controllers/adminController');
const authMiddleware = require('../middlewares/auth');

router.post('/checkout', checkoutController.checkout);

// Admin routes protected by authMiddleware
router.get('/admin/financial-report', authMiddleware, adminController.financialReport);
router.delete('/users/:id', authMiddleware, adminController.deleteUser);

module.exports = router;
