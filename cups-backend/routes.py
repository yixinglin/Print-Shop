
import lib 
from fastapi import FastAPI, File, UploadFile, HTTPException
import os 
from pydantic import BaseModel

app = FastAPI()
history_file_path = os.path.join(os.getcwd(), "history")

# 创建 CUPS 连接
@app.get("/")
def read_root():
    return {"message": "Welcome to the CUPS Print Server"}

@app.get("/printers")
def get_printers():
    try:
        printers = lib.list_printers()
        return {"printers": printers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/attributes/{printer_name}")
def list_printer_attributes(printer_name):
    try:
        attrs = lib.printer_attributes_brief(printer_name)        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    return {"printer_attributes": attrs}

@app.get("/status/{printer_name}")
def list_printer_status(printer_name):
    try:
        status = lib.printer_status(printer_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"printer_status": status}

@app.get("/jobs")
def list_jobs():
    try:
        jobs = lib.print_jobs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"jobs": jobs}


class PrintJob(BaseModel):
    printer_name: str
    filename: str  # filename in the history directory
    title: str = "Print Job"
    options: dict={}


@app.post("/create_job/from-history/")
def create_job_print_history_file(job: PrintJob):
    try:
        file_path = os.path.join(history_file_path, job.filename)
        print(file_path)
        job_id = lib.create_job(job.printer_name, file_path, job.title, job.options)
        return {"job_id": job_id, 
                "status": "Printing initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/history/upload/")
async def update_file_to_history(file: UploadFile):
    if not file:
        return {"message": "No upload file sent"}
    else:
        if file.content_type not in ["application/pdf"]:
            return {"message": "File type not supported. Please upload a PDF file"}
        file_path = os.path.join(history_file_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"filename": file.filename, 
                "path": file_path, 
                "status": "File uploaded successfully"}

@app.delete("/history/clean")         
def clean_history_files():
    try:
        target_dir = history_file_path
        for root, dirs, files in os.walk(target_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "History files cleaned successfully"}
        
@app.get("/history/files")
def list_history_files():
    try:
        files = os.listdir(history_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"files": files, "path": history_file_path, "count": len(files)}


