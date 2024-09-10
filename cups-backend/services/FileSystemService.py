import datetime
import hashlib
import io
import os
import time
from urllib.parse import quote

from fastapi import UploadFile
from starlette.responses import StreamingResponse

import utils.pdfutils as pdfutils
from core.log import logger
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

    async def query_file_by_id(self, id):
        print_file = await self.crud.query_file_by_id(id)
        if print_file:
            return await PrintFile_Pydantic.from_tortoise_orm(print_file)
        else:
            raise RuntimeError(f"File with id [{id}] not found")

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
            logger.info(f"File uploaded with id in database: {id}")

            print_file = await self.crud.query_file_by_id(id)
            # print(f"Print file: {print_file}")
            # print(print_file.file_hash)
            logger.info(f"Print file: {print_file} with hash: {print_file.file_hash}")
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

    def _add_watermark_to_pdf(self, file_path, watermark_text) -> bytes:
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
            pdf_bytes = pdfutils.add_watermark_auto_position(pdf_bytes,
                                                             watermark_text, font_size=7)
        return pdf_bytes

    def generate_watermark_text(self, print_file: T_PrintFile):
        filename = print_file.file_name
        md5_hash = filename + str(time.time())
        md5_hash = hashlib.md5(md5_hash.encode('utf-8')).hexdigest().upper()
        return f"{filename} | {datetime.datetime.now().strftime('%Y.%m.%d_%H:%M')} | <{md5_hash[:5]}>"

    async def download_file(self, hash, embedded=False, enabled_watermark=False):
        try:
            # 获取文件信息
            print_file: T_PrintFile = await self.crud.query_file_by_hash(hash)
            if not print_file:
                raise RuntimeError("File not found")

            # 组合文件路径
            file_path = os.path.join(self.root, f"{print_file.file_hash}.{print_file.file_extension}")
            if not os.path.isfile(file_path):
                raise RuntimeError("File not found")

            # 检查文件类型是否为PDF
            if print_file.file_extension.lower() != "pdf":
                raise RuntimeError("File type not supported. Please download a PDF file")

            # 添加水印并生成PDF流, Filename + datetime + md5
            if enabled_watermark:
                watermark_text = self.generate_watermark_text(print_file)
            else:
                watermark_text = ""
            pdf_bytes = self._add_watermark_to_pdf(file_path, watermark_text)
            pdf_stream = io.BytesIO(pdf_bytes)

            # 创建文件名的URL编码
            encoded_filename = quote(print_file.file_name)

            # 返回StreamingResponse
            return self._create_streaming_response(
                pdf_stream,
                media_type=print_file.file_type,
                filename=encoded_filename,
                embedded=embedded
            )

        except Exception as e:
            raise RuntimeError(str(e))

    def _create_streaming_response(self, pdf_stream, media_type, filename, embedded):
        """生成 StreamingResponse 响应"""
        content_disposition = "inline" if embedded else "attachment"
        headers = {
            "Content-Disposition": f"{content_disposition}; filename*=UTF-8''{filename}"
        }
        return StreamingResponse(pdf_stream, media_type=media_type, headers=headers)

    async def delete_file(self, file_path, file_name):
        pass

    async def archive_file(self, hash, archived=True):
        print_file: T_PrintFile = await self.crud.query_file_by_hash(hash)
        if print_file:
            print_file.archived = archived
            if not archived:
                print_file.print_count = 0
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
            if not archived:
                f.print_count = 0
            await f.save()
        return {
            "message": f"All files have been archived"
        }

    def is_file_exists(self, hash):
        filepath = os.path.join(self.root, f"{hash}.pdf")
        return os.path.isfile(filepath)

    async def list_files(self, file_path="", include_archived=False):
        print_files = await self.crud.query_all_files()
        # Filter file if not exists in file system
        print_files = [f for f in print_files if self.is_file_exists(f.file_hash)]
        if not include_archived:
            print_files = [f for f in print_files if not f.archived]
        print_files.sort(key=lambda x: x.created_at, reverse=True)
        files_pydantic = [await PrintFile_Pydantic.from_tortoise_orm(f) for f in print_files]
        total_size = sum(f.file_size for f in files_pydantic)
        count = len(print_files)
        files = print_files
        return {"total_size": total_size, "count": count, "files": files}

    async def accumulate_print_count(self, hash):
        print_file: T_PrintFile = await self.crud.query_file_by_hash(hash)
        if print_file:
            print_file.print_count += 1
            print_file.last_printed_at = datetime.datetime.now()
            print_file.archived = False
            await print_file.save()
            return {"message": f"Print count (={print_file.print_count}) for file {hash} incremented"}
        else:
            raise RuntimeError(f"File [{hash}] not found")
