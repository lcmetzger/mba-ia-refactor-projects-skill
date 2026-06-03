const db = require('../database/connection');

class AuditModel {
    async log(action) {
        return await db.run("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
    }
}

module.exports = new AuditModel();
