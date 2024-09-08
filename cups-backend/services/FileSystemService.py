import os
from urllib.parse import quote

from fastapi import UploadFile
from starlette.responses import FileResponse

from crud.filesys import PrintFileCRUD
from models import T_PrintFile
from schemas.filesys import PrintFile_Pydantic


class FileSystemService:

    def __init__(self, root):
        self.root = root
        self.crud = PrintFileCRUD()


    async def query_file_by_hash(self, hash):
        print_file = await self.crud.query_file_by_hash(hash)
        if print_file:
            return await PrintFile_Pydantic.from_tortoise_orm(print_file)
        else:
            raise RuntimeError(f"File with hash [{hash}] not found")



    async def upload_file(self, file: UploadFile):
        if not file:
            raise RuntimeError("No file uploaded")
        else:
            if file.content_type not in ["application/pdf"]:
                # raise HTTPException(status_code=400, detail="File type not supported. Please upload a PDF file")
                raise RuntimeError("File type not supported. Please upload a PDF file")
            size_limit = 50 * 1024 * 1024
            if file.size > size_limit:
                raise RuntimeError(f"File size exceeds {size_limit / 1024 / 1024:.2f}MB. Please upload a smaller file")

            # Save to Database
            id = await self.crud.add_file(file, self.root)
            print(f"File uploaded with id in database: {id}")

            print_file = await self.crud.query_file_by_id(id)
            print(f"Print file: {print_file}")
            print(print_file.file_hash)
            hash_value = print_file.file_hash
            file_name = f"{hash_value}.{print_file.file_extension}"
            # Save to File System
            file_path = os.path.join(self.root, file_name)
            await file.seek(0)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            return {"filename": file.filename,
                    "path": file_path,
                    "status": "File uploaded successfully"}

    async def download_file(self, hash, embedded=False):
        # try:
        #     file_path = os.path.join(history_file_path, filename)
        #     print(file_path)
        #     if os.path.isfile(file_path):
        #         # Check if file is PDF
        #         if file_path.endswith(".pdf"):
        #             if not embedded:
        #                 return FileResponse(file_path,
        #                                     media_type="application/pdf",
        #                                     filename=filename)
        #             else:
        #                 encoded_filename = quote(filename)
        #                 return FileResponse(file_path,
        #                                     media_type="application/pdf",
        #                                     filename=filename,
        #                                     headers={
        #                                         "Content-Disposition": "inline; filename*=UTF-8''" + encoded_filename})
        #         else:
        #             raise HTTPException(status_code=400, detail="File type not supported. Please download a PDF file")
        #     else:
        #         raise HTTPException(status_code=404, detail="File not found")
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=str(e))

        try:
            print_file: T_PrintFile = await self.crud.query_file_by_hash(hash)
            if print_file:
                file_path = os.path.join(self.root, f"{print_file.file_hash}.{print_file.file_extension}")
                if os.path.isfile(file_path):
                    # Check if file is PDF
                    if print_file.file_extension.lower() == "pdf":
                        if not embedded:
                            return FileResponse(file_path,
                                                media_type=print_file.file_type,
                                                filename=print_file.file_name)
                        else:
                            encoded_filename = quote(print_file.file_name)
                            return FileResponse(file_path,
                                                media_type=print_file.file_type,
                                                filename=print_file.file_name,
                                                headers={
                                                    "Content-Disposition": "inline; filename*=UTF-8''" + encoded_filename})
                    else:
                        raise RuntimeError("File type not supported. Please download a PDF file")
                else:
                    raise RuntimeError("File not found")
            else:
                raise RuntimeError("File not found")
        except Exception as e:
            raise RuntimeError(str(e))

    async def delete_file(self, file_path, file_name):
        pass

    async def archive_file(self, hash, archived=True):
        print_file: T_PrintFile = await self.crud.query_file_by_hash(hash)
        if print_file:
            print_file.archived = archived
            await print_file.save()
            return {
                "message": f"File {print_file.file_name} has been archived"
            }
        else:
            raise RuntimeError(f"File [{hash}] not found")


    async def archive_all_files(self, archived=True):
        print_files = await self.crud.query_all_files()
        for f in print_files:
            f.archived = archived
            await f.save()
        return {
            "message": f"All files have been archived"
        }

    async def list_files(self, file_path="", include_archived=False):
        print_files = await self.crud.query_all_files()
        if not include_archived:
            print_files = [f for f in print_files if not f.archived]
        print_files.sort(key=lambda x: x.created_at, reverse=True)

        files_pydantic = [await PrintFile_Pydantic.from_tortoise_orm(f) for f in print_files]

        total_size = sum(f.file_size for f in files_pydantic)
        count = len(print_files)
        files = print_files

        return {"total_size": total_size, "count": count, "files": files}

