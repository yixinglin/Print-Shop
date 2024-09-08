from tortoise.models import Model
from tortoise import fields

class T_PrintFile(Model):
    id = fields.IntField(pk=True, generated=True) # primary key
    created_at = fields.DatetimeField(auto_now_add=True, formatter='%Y-%m-%d %H:%M:%S')
    file_name = fields.CharField(max_length=255)
    file_path = fields.CharField(max_length=1024)
    file_hash = fields.CharField(max_length=512, unique=True)
    file_size = fields.IntField(default=0)
    file_type = fields.CharField(max_length=20, null=True)
    file_extension = fields.CharField(max_length=10, default="")
    owner = fields.CharField(max_length=50, default='unknown')
    description = fields.CharField(max_length=1000, default='')
    archived = fields.BooleanField(default=False)
    color = fields.CharField(max_length=20, default='black')
    persistent = fields.BooleanField(default=False)   # whether the file is persistently printed or not
    last_printed_at = fields.DatetimeField(null=True)
    last_printed_by = fields.CharField(max_length=255, null=True)
    print_count = fields.IntField(default=0)

    def __str__(self):
        return self.file_name


