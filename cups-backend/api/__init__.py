import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from core.db import init_db_sqlite
import sys
history_file_path = os.path.join(os.getcwd(), "history")
from .routes.print_history import hist

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