
import os

from fastapi import APIRouter, HTTPException

import services.lib as lib
from api import history_file_path
from models import T_PrintFile
from services.FileSystemService import FileSystemService

cups = APIRouter(prefix="/cups", tags=["CUPS Backend"])



# 创建 CUPS 连接
@cups.get("/")
def read_root():
    return {"message": "Welcome to the CUPS Print Server"}

@cups.get("/printers")
def get_printers():
    try:
        printers = lib.list_printers()
        return {"printers": printers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@cups.get("/attributes/{printer_name}")
def list_printer_attributes(printer_name):
    try:
        attrs = lib.printer_attributes_brief(printer_name)        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    return {"printer_attributes": attrs}

@cups.get("/status/{printer_name}")
def list_printer_status(printer_name):
    try:
        status = lib.printer_status(printer_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"printer_status": status}

@cups.get("/jobs")
def list_jobs():
    try:
        jobs = lib.print_jobs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"jobs": jobs}

@cups.get("/jobs/{job_id}")
def get_job_attributes(job_id: int):
    try:
        attrs = lib.job_attributes(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"job_attributes": attrs}


@cups.delete("/jobs/cancel/{job_id}")
def cancel_print_job(job_id: int):
    try:
        lib.cancel_job(job_id)
        return {"status": "Print job cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@cups.delete("/jobs/cancel/all/")
def cancel_all_print_jobs():
    try:
        ans = lib.cancel_all_jobs()
        print(ans)
        return {"status": "All print jobs cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@cups.post("/jobs/create/from_history/")
def create_job_print_history_file(job: lib.PrintJob):
    try:
        # file_path = os.path.join(history_file_path, job.filename)
        svc = FileSystemService(history_file_path)
        print_file: T_PrintFile = asyncio.run(svc.query_file_by_hash(job.hash))
        # print(file_path)
        file_path = os.path.join(history_file_path, print_file.file_hash+'.'+print_file.file_extension)
        print("Job Created: ", job)
        job_id = lib.create_job(job.printer_name, file_path, job.title, job.options)
        return {"job_id": job_id, 
                "status": "Printing initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from .connection import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json 

manager = ConnectionManager()

@cups.websocket("/ws/printer/{printer_name}")
async def websocket_endpoint(printer_name: str, websocket: WebSocket):
    await manager.connect(websocket)
    count = 0
    try:
        while True:
            # 在这里可以根据实际情况获取打印机状态并发送给客户端
            # 比如：message = get_printer_status()
            # Process id
            pid = os.getpid()
            print(f"ws[{pid}-{count}]: Sending printer status for {printer_name}")
            # status = lib.printer_attributes_brief(printer_name)                        
            printers = lib.list_printers()
            printers = [p for p in printers if p['printer-name'] == printer_name]
            jobs = lib.print_jobs()
            if len(printers) > 0:
                printer = printers[0]
            else:
                raise RuntimeError(f"Printer {printer_name} not found")
            message = json.dumps(printer)
            await manager.send_message(message)                        
            await asyncio.sleep(1)     
            count += 1       
    except (WebSocketDisconnect, Exception) as e:    
        print("ws: Disconnected--: ", e)
        manager.disconnect(websocket)

