const db = require('../database/connection');

class ReportService {
    async getFinancialReport() {
        // Solving N+1 with a JOIN
        const sql = `
            SELECT 
                c.title as course_title,
                u.name as student_name,
                p.amount as payment_amount,
                p.status as payment_status
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN users u ON u.id = e.user_id
            LEFT JOIN payments p ON p.enrollment_id = e.id
        `;
        
        const rows = await db.all(sql);
        
        const reportMap = {};
        
        rows.forEach(row => {
            if (!reportMap[row.course_title]) {
                reportMap[row.course_title] = { course: row.course_title, revenue: 0, students: [] };
            }
            
            if (row.student_name) {
                if (row.payment_status === 'PAID') {
                    reportMap[row.course_title].revenue += row.payment_amount;
                }
                reportMap[row.course_title].students.push({
                    student: row.student_name,
                    paid: row.payment_amount || 0
                });
            }
        });
        
        return Object.values(reportMap);
    }
}

module.exports = new ReportService();
