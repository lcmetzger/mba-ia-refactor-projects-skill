const db = require('../database/connection');

class CourseModel {
    async findActiveById(id) {
        return await db.get("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    }

    async findAll() {
        return await db.all("SELECT * FROM courses");
    }
}

module.exports = new CourseModel();
