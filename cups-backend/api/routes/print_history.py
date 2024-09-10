import os
from fastapi import APIRouter, UploadFile, HTTPException

from api import history_file_path
from services.FileSystemService import FileSystemService


hist = APIRouter(prefix="/history", tags=["Print History"])

@hist.post("/upload/")
async def update_file_to_history(file: UploadFile):
    try:
        svc = FileSystemService(history_file_path)
        result = await svc.upload_file(file)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


# @hist.delete("/empty")
# def clean_all_history_files():
#     try:
#         target_dir = history_file_path
#         for root, dirs, files in os.walk(target_dir, topdown=False):
#             for name in files:
#                 os.remove(os.path.join(root, name))
#             for name in dirs:
#                 os.rmdir(os.path.join(root, name))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return {"status": "History files cleaned successfully"}

# @hist.delete("/file/{filename}")
# def delete_file_from_history(filename):
#     try:
#         file_path = os.path.join(history_file_path, filename)
#         os.remove(file_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return {"status": "File deleted successfully"}

@hist.delete("/file/archive-all")
async def archive_all_files_from_history():
    try:
        svc = FileSystemService(history_file_path)
        return await svc.archive_all_files()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@hist.delete("/file/archive/{hash}")
async def archive_file_from_history_by_hash(hash):
    try:
        svc = FileSystemService(history_file_path)
        return await svc.archive_file(hash, archived=True)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@hist.put("/file/unarchive/{hash}")
async def unarchive_file_from_history_by_hash(hash):
    try:
        svc = FileSystemService(history_file_path)
        return await svc.archive_file(hash, archived=False)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@hist.get("/files")
async def list_history_files(include_archived:bool=False):
    try:
        svc = FileSystemService(history_file_path)
        result = await svc.list_files(include_archived=include_archived)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

@hist.get("/file/down/{hash}")
async def download_history_file(hash, embedded:bool=False, enabled_watermark:bool=False):
    try:
        svc = FileSystemService(history_file_path)
        return await svc.download_file(hash, embedded=embedded, enabled_watermark=enabled_watermark)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@hist.put("/file/print-count/1/{hash}")
async def accumulate_print_count(hash):
    try:
        svc = FileSystemService(history_file_path)
        return await svc.accumulate_print_count(hash)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))