import os
from fastapi import APIRouter, UploadFile, HTTPException

from api import history_file_path
from services.FileSystemService import FileSystemService


hist = APIRouter(prefix="/history", tags=["Print History"])

@hist.post("/upload/")
async def update_file_to_history(file: UploadFile):
    # if not file:
    #     return {"message": "No upload file sent"}
    # else:
    #     if file.content_type not in ["application/pdf"]:
    #         # return {"message": "File type not supported. Please upload a PDF file"}
    #         raise HTTPException(status_code=400, detail="File type not supported. Please upload a PDF file")
    #     # Prevent size > 50MB
    #     size_limit = 50*1024*1024
    #     if file.size > size_limit:
    #         return {"message": f"File size exceeds {size_limit/1024/1024:.2f}MB. Please upload a smaller file"}
    #
    #     file_path = os.path.join(history_file_path, file.filename)
    #     with open(file_path, "wb") as buffer:
    #         buffer.write(await file.read())
    #
    #     return {"filename": file.filename,
    #             "path": file_path,
    #             "status": "File uploaded successfully"}

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
    # try:
    #     files = os.listdir(history_file_path)
    #     infos = []
    #     sum_size = 0
    #     for filename in files:
    #         file_path = os.path.join(history_file_path, filename)
    #         if os.path.isfile(file_path):
    #             size = os.path.getsize(file_path)
    #             size_str = utils.convert_bytes_to_human_readable_size(size)
    #             create_at = os.path.getctime(file_path)
    #             create_at = datetime.datetime.fromtimestamp(create_at).strftime('%Y-%m-%d %H:%M:%S')
    #             file_info = {"filename": filename,
    #                         "create_at": create_at,
    #                         "size": size_str }
    #             infos.append(file_info)
    #             sum_size += size
    #     infos.sort(key=lambda x: x["create_at"], reverse=True)
    #     sum_size_str = utils.convert_bytes_to_human_readable_size(sum_size)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # return {"path": history_file_path,
    #         "total_size": sum_size_str,
    #         "count": len(files),
    #         "files": infos, }

    try:
        svc = FileSystemService(history_file_path)
        result = await svc.list_files(include_archived=include_archived)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

@hist.get("/down/{hash}")
async def download_history_file(hash, embedded:bool=False):
    try:
        svc = FileSystemService(history_file_path)
        return await svc.download_file(hash, embedded)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
