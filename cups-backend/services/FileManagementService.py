"""
管理打印的文件
"""
from pydantic import BaseModel

from core.log import server_logger as logger
from core.config import server_config as config

class PrintFile(BaseModel):
    """
    打印文件类
    """
    id: str
    filename: str
    path: str
    print_count: int = 0
    last_print_time: str = ""


class FileManagementService:

    def __init__(self):
        pass

