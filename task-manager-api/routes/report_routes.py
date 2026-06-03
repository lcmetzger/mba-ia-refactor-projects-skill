from flask import Blueprint
from controllers.report_controller import ReportController

report_bp = Blueprint('reports', __name__)

report_bp.route('/reports/summary', methods=['GET'])(ReportController.summary)
report_bp.route('/reports/productivity', methods=['GET'])(ReportController.user_productivity)
report_bp.route('/categories', methods=['GET'])(ReportController.list_categories)
report_bp.route('/categories', methods=['POST'])(ReportController.create_category)
report_bp.route('/categories/<int:cat_id>', methods=['PUT'])(ReportController.update_category)
report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])(ReportController.delete_category)
