import logging

from fastapi import FastAPI
import uvicorn


from dotenv import load_dotenv
load_dotenv()


from app.store_monitor_app.api.v1 import store_monitor
from app.store_app.api.v1 import store
from app.crons import store_status_polling_cron


app = FastAPI()
logger = logging.getLogger("uvicorn.access")

# routers registration
app.include_router(store_monitor.router, prefix="/v1", tags=["store monitoring v1"])
app.include_router(store.router, prefix="/v1", tags=["store details"])


@app.on_event("startup")
async def startup_event():
    print("startup event triggered")
    store_status_polling_cron.run_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    print("shutdown event triggered")
    store_status_polling_cron.stop_scheduler()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
