const db = require('../database/connection');

class EnrollmentModel {
    async create(userId, courseId) {
        const result = await db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [userId, courseId]);
        return result.lastID;
    }

    async findByCourseId(courseId) {
        return await db.all("SELECT * FROM enrollments WHERE course_id = ?", [courseId]);
    }
}

module.exports = new EnrollmentModel();
