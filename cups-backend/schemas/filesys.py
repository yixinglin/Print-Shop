from typing import Optional

from pydantic.v1 import root_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from models.filesys import T_PrintFile

PrintFile_Pydantic = pydantic_model_creator(T_PrintFile, name="PrintFile", )







