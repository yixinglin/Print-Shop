from typing import List, Dict

from pydantic import BaseModel, Field

class PrintJob(BaseModel):
    id: str = Field("", description="Unique identifier for the print job")
    client_id: str
    user: str
    printer_name: str
    filename: str  # filename in the history directory
    title: str = "Print Job"
    options: dict={}


class PrinterRegistration(BaseModel):
    client_id: str
    attrs: List[Dict]
    total: int

class JobStatusUpdate(BaseModel):
    client_id: str
    job_id: str
    attrs: Dict