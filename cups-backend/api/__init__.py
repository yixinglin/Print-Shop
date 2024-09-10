import sys

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from core.config import cups_client_config as config
from core.db import init_db_sqlite
history_file_path = config.history.path
log_file_path = config.logging.path


from .routes.print_history import hist
from services.scheduler import scheduler
from core.log import logger

if sys.platform == "linux":
    from .routes.cups_routes import cups
else:
    cups = APIRouter(prefix="/cups")



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



cups.include_router(hist)
app.include_router(cups)

init_db_sqlite(app)


@app.on_event("startup")
def app_start():
    print("FastAPI app started_")
    logger.info("FastAPI app started")
    logger.info(config)
    scheduler.start()

@app.on_event("shutdown")
def app_stop():
    print("FastAPI app stopped")
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Welcome to Print Server API"}