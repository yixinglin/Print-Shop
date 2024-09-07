from fastapi import APIRouter
from .printer import printer_router
from .filesys import filesys_router
from .printjob import job_router


v2 = APIRouter(prefix="/v2", )

v2.include_router(printer_router, tags=["Printer"])
v2.include_router(job_router, tags=["Print Job"])
v2.include_router(filesys_router, tags=["File System"])
