from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from utils import StrUtil
import datetime
from urllib.parse import quote
import os
history_file_path = os.path.join(os.getcwd(), "history")

hist = APIRouter(prefix="/history", tags=["Print History"])

@hist.post("/upload/")
async def update_file_to_history(file: UploadFile):
    if not file:
        return {"message": "No upload file sent"}
    else:
        if file.content_type not in ["application/pdf"]:
            # return {"message": "File type not supported. Please upload a PDF file"}
            raise HTTPException(status_code=400, detail="File type not supported. Please upload a PDF file")
        # Prevent size > 50MB
        size_limit = 50*1024*1024
        if file.size > size_limit:
            return {"message": f"File size exceeds {size_limit/1024/1024:.2f}MB. Please upload a smaller file"}

        file_path = os.path.join(history_file_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"filename": file.filename, 
                "path": file_path, 
                "status": "File uploaded successfully"}

@hist.delete("/empty")         
def clean_all_history_files():
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

@hist.delete("/file/{filename}")
def delete_file_from_history(filename):
    try:
        file_path = os.path.join(history_file_path, filename)
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "File deleted successfully"}

@hist.get("/files")
def list_history_files():
    try:
        files = os.listdir(history_file_path)
        infos = []
        sum_size = 0
        for filename in files:
            file_path = os.path.join(history_file_path, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                size_str = utils.convert_bytes_to_human_readable_size(size)
                create_at = os.path.getctime(file_path)                  
                create_at = datetime.datetime.fromtimestamp(create_at).strftime('%Y-%m-%d %H:%M:%S')
                file_info = {"filename": filename, 
                            "create_at": create_at, 
                            "size": size_str }
                infos.append(file_info)
                sum_size += size
        infos.sort(key=lambda x: x["create_at"], reverse=True)
        sum_size_str = utils.convert_bytes_to_human_readable_size(sum_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"path": history_file_path, 
            "total_size": sum_size_str, 
            "count": len(files), 
            "files": infos, }

@hist.get("/down/{filename}")
def download_history_file(filename, embedded:bool=False):
    try:
        file_path = os.path.join(history_file_path, filename)
        print(file_path)
        if os.path.isfile(file_path):
            # Check if file is PDF
            if file_path.endswith(".pdf"):
                if not embedded:
                    return FileResponse(file_path,
                                         media_type="application/pdf", 
                                         filename=filename)
                else:
                    encoded_filename = quote(filename)
                    return FileResponse(file_path, 
                                        media_type="application/pdf", 
                                        filename=filename, 
                                        headers={"Content-Disposition": "inline; filename*=UTF-8''"+encoded_filename })
            else:
                raise HTTPException(status_code=400, detail="File type not supported. Please download a PDF file")
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
