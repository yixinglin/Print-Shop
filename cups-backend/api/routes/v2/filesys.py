from fastapi import UploadFile, APIRouter

filesys_router = APIRouter(prefix="/filesys")

@filesys_router.post("/upload")
def upload_file(file: UploadFile):
    # TODO 上传文件到服务器，可以用于提前上传文件然后在创建打印任务时选择这些文件。
    pass

def delete_uploaded_file(file_id: str):
    # TODO 删除上传到服务器的文件。
    pass

def download_file(file_id: str):
    # TODO 下载服务器上已上传的文件。
    pass

def get_file_list():
    # TODO 获取服务器上已上传的文件列表。
    pass

