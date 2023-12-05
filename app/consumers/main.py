from app.consumers.factory.store_report_generation_factory import StoreReportGenerationFactory

if __name__ == "__main__":
    store_report_generation_factory = StoreReportGenerationFactory.get_store_report_generation_factory().start()
