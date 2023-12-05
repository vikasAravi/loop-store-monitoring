from apscheduler.schedulers.background import BackgroundScheduler

from app.service.store_status_polling_cron_factory import StoreStatusPollingCronFactory

scheduler = BackgroundScheduler()

store_status_poll_cron_factory = StoreStatusPollingCronFactory.get_store_status_polling_cron_factory()


@scheduler.scheduled_job("interval", minutes=1)
def poll_store_status():
    store_status_poll_cron_factory.init_store_status_poll()


def run_scheduler():
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
