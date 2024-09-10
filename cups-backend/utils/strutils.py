

def convert_bytes_to_human_readable_size(size: int):
    return f"{size/1024/1024:.2f} MB" if size > 1024*1024 else f"{size/1024:.2f} KB" if size > 1024 else f"{size} bytes"

def isEmptyString(string: str):
    return string is None or string.strip() == ""