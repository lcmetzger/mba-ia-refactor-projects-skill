const db = require('../database/connection');

class PaymentModel {
    async create(enrollmentId, amount, status) {
        const result = await db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [enrollmentId, amount, status]);
        return result.lastID;
    }

    async findByEnrollmentId(enrollmentId) {
        return await db.get("SELECT amount, status FROM payments WHERE enrollment_id = ?", [enrollmentId]);
    }
}

module.exports = new PaymentModel();
