import traceback

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from api.routes.v2 import v2
from api.routes.cups.task import task_router
from core.config import server_config as config
import core.log as log
from schemas.basic import CodeEnum

app = FastAPI(
    title=config.project_name,
    summary=config.summary,
    version=config.version,
    openapi_url="/api/v2/openapi.json",
    docs_url="/api/docs",
    contact={
        "name": config.author,
        "url": config.url,
        "email": config.email
    }

)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_ = APIRouter(prefix="/api")
api_.include_router(v2)
api_.include_router(task_router)

app.include_router(api_)


logger = log.server_logger

@app.on_event("startup")
async def startup_event():
    logger.info("Server started")
    logger.info(config)



@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stopping scheduler")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    err_detail = traceback.format_exc()
    logger.error(f"An exception occurred: {err_detail}")
    return JSONResponse(status_code=int(CodeEnum.InternalServerError.value),
                        content={"message": f"Internal server error. \n{exc}"})


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    """
    Runtime exception handler
    """
    logger.error(f"A runtime error occurred: {exc}")
    return JSONResponse(status_code=int(CodeEnum.Fail.value),
                        content={"message": str(exc)})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log requests
    """
    # Record request information, including client IP address
    client_ip = request.client.host
    logger.info(f"Request: {request.method} {request.url}, Client IP: {client_ip}")
    # Continue processing the request
    response = await call_next(request)
    # Return response information
    logger.info(f"Response: {response.status_code}")
    # response.headers["Cache-Control"] = "max-age=3600, public"
    # headers = {"Cache-Control": "max-age=3600, public"},
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to to the print shop API"}

