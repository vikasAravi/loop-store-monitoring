import os


def get_reports_path(request_id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'reports', f'store_metrics_report_{request_id}.csv')
    return report_path
