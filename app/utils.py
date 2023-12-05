import os


def get_reports_path(request_id):
    parent_directory = "/Users/vikash/PycharmProjects/loop/app/reports"
    file_name = parent_directory + f"/store_metrics_report_{request_id}.csv"
    return file_name
