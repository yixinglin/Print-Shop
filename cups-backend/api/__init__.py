
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .routes.cups_routes import cups
from .routes.print_history import hist, history_file_path



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cups.include_router(hist)

# app.include_router(cups)
