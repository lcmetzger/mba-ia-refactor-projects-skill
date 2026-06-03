const reportService = require('../services/reportService');

class AdminController {
    async financialReport(req, res) {
        try {
            const report = await reportService.getFinancialReport();
            return res.json(report);
        } catch (error) {
            console.error(error);
            return res.status(500).json({ error: "Internal Server Error" });
        }
    }

    async deleteUser(req, res) {
        const { id } = req.params;
        const userModel = require('../models/UserModel');
        try {
            await userModel.delete(id);
            return res.send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
        } catch (error) {
            console.error(error);
            return res.status(500).json({ error: "Internal Server Error" });
        }
    }
}

module.exports = new AdminController();
