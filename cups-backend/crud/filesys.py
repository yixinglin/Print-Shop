import hashlib
import time

from fastapi import UploadFile
from tortoise.exceptions import IntegrityError

from models.filesys import T_PrintFile
from schemas.filesys import PrintFile_Pydantic


class PrintFileCRUD:
    def __init__(self):
        pass


    async def add_file(self, file: UploadFile, file_path: str):
        # Convert file name + time to md5 hash
        data = await file.read()
        # Generate hash object from file content
        hash_object = hashlib.md5(data)
        print(f"Adding file: {file.filename}; {hash_object.hexdigest()}")
        # Extract file extension
        name_split = file.filename.split(".")
        if len(name_split) > 1:
            ext = name_split[-1].lower()
        else:
            raise RuntimeError("File name should have an extension!")

        # Check if file with same hash already exists
        print_file = await self.query_file_by_hash(hash_object.hexdigest())
        if print_file:
            print(f"File with hash {hash_object.hexdigest()} already exists!")
            print_file.archived = False
            print_file.file_name = file.filename
            await print_file.save()
            return print_file.id

        print_file = T_PrintFile(
            file_name=file.filename,
            file_path=file_path,
            file_hash=hash_object.hexdigest(),
            file_size=file.size,
            file_type=file.content_type,
            file_extension=ext,
        )

        try:
            await print_file.save()
        except IntegrityError as e:
            raise RuntimeError(f"Error adding file: {e}")

        # Return ID of the added file
        return print_file.id

    async def query_file_by_hash(self, hash: str):
        file = await T_PrintFile.get_or_none(file_hash=hash)
        return file

    async def query_file_by_id(self, file_id: int):
        file = await T_PrintFile.get(id=file_id)
        return file

    async def query_all_files(self):
        files = await T_PrintFile.all()
        return files

    async def delete_file(self, file_id: int):
        file = await T_PrintFile.get(id=file_id)
        if not file:
            raise RuntimeError(f"File with ID {file_id} not found")
        await file.delete()
        return True

    async def update_file(self, file_id: int, file_name: str,
                          file_path: str,
                          description: str):
        file = await T_PrintFile.get(id=file_id)
        if not file:
            raise RuntimeError(f"File with ID {file_id} not found")
        file.file_name = file_name
        file.file_path = file_path
        file.file_hash = hashlib.md5((file_name + str(time.time())).encode()).hexdigest()
        file.description = description
        await file.save()
        return file.id



