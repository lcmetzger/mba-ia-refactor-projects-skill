const userModel = require('../models/UserModel');
const courseModel = require('../models/CourseModel');
const enrollmentModel = require('../models/EnrollmentModel');
const paymentModel = require('../models/PaymentModel');
const auditModel = require('../models/AuditModel');
const cryptoService = require('../services/cryptoService');
const cacheService = require('../services/cacheService');
const config = require('../config');

class CheckoutController {
    async checkout(req, res) {
        const { usr, eml, pwd, c_id, card } = req.body;

        if (!usr || !eml || !c_id || !card) {
            return res.status(400).json({ error: "Bad Request" });
        }

        try {
            const course = await courseModel.findActiveById(c_id);
            if (!course) {
                return res.status(404).json({ error: "Curso não encontrado" });
            }

            let user = await userModel.findByEmail(eml);
            let userId;

            if (!user) {
                const hash = cryptoService.badCrypto(pwd || "123456");
                userId = await userModel.create(usr, eml, hash);
            } else {
                userId = user.id;
            }

            console.log(`Processando cartão ${card} na chave ${config.paymentGatewayKey}`);
            const status = card.startsWith("4") ? "PAID" : "DENIED";

            if (status === "DENIED") {
                return res.status(400).json({ error: "Pagamento recusado" });
            }

            const enrollmentId = await enrollmentModel.create(userId, c_id);
            await paymentModel.create(enrollmentId, course.price, status);
            await auditModel.log(`Checkout curso ${c_id} por ${userId}`);

            cacheService.logAndCache(`last_checkout_${userId}`, course.title);

            return res.status(200).json({ msg: "Sucesso", enrollment_id: enrollmentId });
        } catch (error) {
            console.error(error);
            return res.status(500).json({ error: "Internal Server Error" });
        }
    }
}

module.exports = new CheckoutController();
