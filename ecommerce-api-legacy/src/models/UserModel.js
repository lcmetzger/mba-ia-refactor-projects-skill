const db = require('../database/connection');

class UserModel {
    async findByEmail(email) {
        return await db.get("SELECT * FROM users WHERE email = ?", [email]);
    }

    async findById(id) {
        return await db.get("SELECT * FROM users WHERE id = ?", [id]);
    }

    async create(name, email, password) {
        const result = await db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, password]);
        return result.lastID;
    }

    async delete(id) {
        return await db.run("DELETE FROM users WHERE id = ?", [id]);
    }
}

module.exports = new UserModel();
